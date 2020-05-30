from django.urls import path

from noraslunch import views

app_name = "noraslunch"
urlpatterns = [
    # Views
    path('', views.index, name='index'),
    path('menu_list/', views.MenuList.as_view(), name='menu_list'),
    path('crear_menu/', views.CreateMenuView.as_view(), name='create_menu'),
    path('menu_detail/<str:id>/', views.MenuDetailView.as_view(), name='menu_detail'),
    path('menu/<str:id>/', views.CreateEmployeeMealView.as_view(), name='menu'),
    path('thanks/', views.thanks, name='thanks'),
    path('timeout/', views.timeout, name='timeout'),
    path('send_menu/<str:id>/', views.send_menu_as_slack_message, name='send_menu_as_slack_message'),
]
