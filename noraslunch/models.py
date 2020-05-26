import uuid

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    user = models.ForeignKey(User, verbose_name='usuario', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Menu(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu_date = models.DateField('día')

    def get_absolute_url(self):
        return "/menu/%s/" % str(self.id)

    @property
    def meal_options(self):
        return ", ".join([meal.description for meal in self.meal_set.all()])


class Meal(BaseModel):
    description = models.CharField('almuerzo', max_length=200)
    menu = models.ForeignKey('Menu', verbose_name='menu', on_delete=models.CASCADE)


class EmployeeMeal(BaseModel):
    employee_name = models.CharField('nombre', max_length=200)
    meal = models.ForeignKey(Meal, verbose_name='almuerzo', on_delete=models.CASCADE)
    customization = models.CharField('especificación', max_length=200)

