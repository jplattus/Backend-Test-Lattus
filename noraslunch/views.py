import datetime
from uuid import UUID

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView

from noraslunch.forms import MealFormset, EmployeeMealForm
from noraslunch.models import Menu, EmployeeMeal
from noraslunch.tasks import send_slack


def index(request):
    return render(request, 'noraslunch/index.html')


class MenuList(LoginRequiredMixin, ListView):
    queryset = Menu.objects.order_by('-created_at')
    context_object_name = 'menu_list'
    template_name = 'noraslunch/menu_list.html'


class CreateMenuView(LoginRequiredMixin, CreateView):
    model = Menu
    fields = ["menu_date"]
    template_name = "noraslunch/create_menu.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["meals"] = MealFormset(self.request.POST)
        else:
            data["meals"] = MealFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        meals = context["meals"]

        # Debug to find out how formset data is sent
        # print(self.request.POST)

        form.instance.user = self.request.user
        menu = form.save()
        if meals.is_valid():
            for meal in meals.forms:
                m = meal.save(commit=False)
                m.menu = menu
                m.user = self.request.user
                m.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("noraslunch:menu_detail", kwargs={'id': str(self.object.id)})


class MenuDetailView(LoginRequiredMixin, DetailView):
    template_name = 'noraslunch/menu_detail.html'
    model = Menu

    def get_object(self):
        # We need to check UUID first. If uuid not valid, simply throw 404 error
        try:
            uuid = UUID(self.kwargs['id'], version=4)
        except ValueError:
            raise Http404
        menu = get_object_or_404(Menu, id=uuid)
        return menu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['meal_orders'] = EmployeeMeal.objects.filter(meal__menu=self.object).order_by('meal')
        return context


class CreateEmployeeMealView(CreateView):
    model = EmployeeMeal
    form_class = EmployeeMealForm

    def get_template_names(self):
        dt = datetime.datetime.now()
        if dt.time() < datetime.time(11):
            template_name = "noraslunch/create_employee_meal.html"
        else:
            template_name = "noraslunch/timeout.html"
        return template_name

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['menu_id'] = self.kwargs.get('id')
        return kwargs

    def form_valid(self, form):
        # Dont save if its before 11 AM CLT
        dt = datetime.datetime.now()
        if dt.time() > datetime.time(11):
            return reverse("noraslunch:timeout")

        # Employee meal needs to inherit meal user
        form.instance.user = form.instance.meal.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("noraslunch:thanks")


def thanks(request):
    return render(request, 'noraslunch/thanks.html')


def timeout(request):
    return render(request, 'noraslunch/timeout.html')


@login_required
def send_menu_as_slack_message(request, id):
    menu = get_object_or_404(Menu, id=id)
    if send_slack.delay(menu.id) and not menu.was_sent:
        menu.was_sent = True
        menu.save()
        messages.success(request, 'El mensaje fue enviado.')
    else:
        messages.error(request, 'Ocurrió un error en el envío')

    return HttpResponseRedirect(reverse("noraslunch:menu_detail", kwargs={'id': str(id)}))
