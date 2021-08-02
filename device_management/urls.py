from django.urls import path
from . import views

app_name = 'device_management'

urlpatterns =[
    path('add/', views.device_add, name='device_add'),
    path('edit/<int:pk>/', views.device_edit, name='device_edit'),
    path('list/inactive/', views.device_list_inactive, name='device_list_inactive'),
    path('list/active/', views.device_list_active, name='device_list_active'),
    path('activate/<int:pk>/', views.device_activate, name='device_activate'),
    path('deactivate/<int:pk>/', views.device_deactivate, name='device_deactivate'),
    path('reset/<int:pk>/', views.device_reset, name='device_reset'),
]