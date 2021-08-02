from django.urls import path
from . import views


app_name = 'user_management'

urlpatterns =[

    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('login_validate/', views.login_validate, name='login_validate'),
    path('user_reg/', views.user_registration, name='user_reg'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_user/<int:pk>/', views.reset_password_of_particular_user,
         name='reset_password_of_particular_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('user_profile/<int:pk>/', views.user_profile, name='user_profile'),
    path('organization_reg/', views.organization_reg, name='organization_reg'),
    path('organization_list/', views.organization_list, name='organization_list'),
    path('organization_edit/<int:pk>/', views.organization_edit, name='organization_edit'),
    path('organization_delete/<int:pk>/', views.organization_delete, name='organization_delete'),



]

