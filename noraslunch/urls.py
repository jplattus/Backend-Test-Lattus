from django.urls import path

from noraslunch import views

urlpatterns = [
    # Views
    path('', views.index, name='index'),
    path('home/', views.MenuList.as_view(), name='home'),
    path('crear_menu/', views.MenuCreateView.as_view(), name='create_menu'),
    path('menu_detail/<str:id>/', views.MenuDetailView.as_view(), name='menu_detail'),
    path('menu/<str:id>/', views.EmployeeMealCreateView.as_view(), name='menu'),
    path('thanks/', views.thanks, name='thanks'),
]