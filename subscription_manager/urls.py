"""
URL configuration for subscription_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from subscriptions import views as subscriptions_views
from subscriptions.views import create_admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('subscriptions/', include('subscriptions.urls')),

    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', subscriptions_views.custom_logout, name='logout'),

    # Регистрация
    path('register/', subscriptions_views.register, name='register'),

    # Профиль и смена пароля
    path('profile/', subscriptions_views.profile, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='auth/password_change.html',
        success_url='/profile/'
    ), name='password_change'),

    path('pay/<int:pk>/', subscriptions_views.pay_now, name='pay_now'),

    path('profile/edit/', subscriptions_views.profile_edit, name='profile_edit'),

    path("create-admin/", create_admin),
]