from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name="user/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change_form/', views.change_password, name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]

