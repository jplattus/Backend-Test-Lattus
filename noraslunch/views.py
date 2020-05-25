from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader, Context


def index(request):
    return render(request, 'noraslunch/index.html')


def create_menu(request):
    return render(request, 'noraslunch/create_menu.html')


def menu_detail(request):
    return render(request, 'noraslunch/menu_detail.html')
