from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # Page 1: username + password form
    path(
        '',
        auth_views.LoginView.as_view(
            template_name='login.html',
            redirect_authenticated_user=True,
        ),
        name='login',
    ),
    # Page 2: welcome text (login required)
    path('welcome/', views.welcome, name='welcome'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]