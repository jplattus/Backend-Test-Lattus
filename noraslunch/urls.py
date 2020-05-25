from django.urls import path

from noraslunch import views

urlpatterns = [
    # Views
    path('', views.index, name='index'),
    path('crear_menu/', views.create_menu, name='create_menu'),
    path('menu/', views.menu_detail, name='menu_detail'),
]