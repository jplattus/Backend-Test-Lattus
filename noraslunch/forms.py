from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet, SelectDateWidget

from noraslunch.models import Menu, Meal


class MenuForm(forms.ModelForm):
    menu_date = forms.DateField(input_formats=['%m %d %Y'], widget=SelectDateWidget)

    class Meta:
        model = Menu
        exclude = ['user', 'created_at']


MealFormset = inlineformset_factory(Menu, Meal, fields=['description'], extra=5)

