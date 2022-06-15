"""pochvenscouts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from pochven import views

urlpatterns = [
    path("", views.RootView.as_view(), name="root"),

    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.Logout.as_view(), name="logout"),

    path(
        "accounts/register/",
        views.RegistrationView.as_view(success_url="/profile/"),
        name="django_registration_register",
    ),
    path(
        "accounts/change-password/",
         auth_views.PasswordChangeView.as_view(template_name="accounts/password_change_form.html"),
         name='change-password'),

    path(
        "accounts/change-password/done/",
        TemplateView.as_view(template_name="accounts/password_change_done.html"),
        name="password_change_done"),

    path(
        "accounts/password-reset/",
        PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="password_reset"),

    path(
        "accounts/password-reset/done/",
        PasswordResetView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done"),

    path(
        "accounts/password/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
        name="password_reset_confirm"),

    path(
        "accounts/password/reset/done/",
        PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete"),



    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
