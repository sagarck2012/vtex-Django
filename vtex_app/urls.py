from django.urls import path
from . import views

app_name = 'viyellatex'

urlpatterns =[

    path('home/', views.home, name='home'),
    path('home/get_machine_data/', views.get_machine_data, name='get_machine_data'),
    path('home/detail/<int:pk>/', views.detail, name='detail'),
    path('home/detail/<int:pk>/get_chart_data', views.get_chart_data, name='get_chart_data'),


]
