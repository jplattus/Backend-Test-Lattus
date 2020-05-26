
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader, Context
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView

from noraslunch.forms import MenuForm, MealFormset
from noraslunch.models import Menu, EmployeeMeal


def index(request):
    return render(request, 'noraslunch/index.html')


class MenuList(LoginRequiredMixin, ListView):
    queryset = Menu.objects.order_by('-created_at')
    context_object_name = 'menu_list'
    template_name = 'noraslunch/home.html'


class MenuCreateView(LoginRequiredMixin, CreateView):
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
        return reverse("home")


class MenuDetailView(LoginRequiredMixin, DetailView):
    template_name = 'noraslunch/menu_detail.html'
    model = Menu

    def get_object(self):
        menu = get_object_or_404(Menu, id=self.kwargs['id'])
        return menu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['meal_orders'] = EmployeeMeal.objects.filter(meal__menu=self.object)
        return context


