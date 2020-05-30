from uuid import UUID

from django import forms
from django.forms import inlineformset_factory, SelectDateWidget
from django.http import Http404
from django.shortcuts import get_object_or_404

from noraslunch.models import Menu, Meal, EmployeeMeal


class MenuForm(forms.ModelForm):
    menu_date = forms.DateField()

    class Meta:
        model = Menu
        exclude = ['user', 'created_at']


MealFormset = inlineformset_factory(Menu, Meal, fields=['description'], extra=0, can_delete=True)


class EmployeeMealForm(forms.ModelForm):
    class Meta:
        model = EmployeeMeal
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'meal': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        """
        This is used to filter the meals options
        As the menu has uuid id, the app throw UUID validation error 500 if someone change the url
        So it becomes necessary to check uuid before get the menu object.
        If its not valid, simply raise 404 error
        """

        try:
            uuid = UUID(kwargs.pop('menu_id', None), version=4)
        except ValueError:
            raise Http404
        menu = get_object_or_404(Menu, id=uuid)

        super().__init__(*args, **kwargs)

        # Override queryset of this menu meals
        self.fields['meal'].queryset = self.fields['meal'].queryset.filter(menu=menu)
