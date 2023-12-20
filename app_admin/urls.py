from django.contrib import admin
from django.urls import path

from app_admin.views import (
    RegisterView,
    AdminRegisterView,
    AdminLoginViews,
)


urlpatterns = [
    path('Register-User/',RegisterView.as_view()),
    path("Register-Admin-User/", AdminRegisterView.as_view(), name="RegisterAdminUser"),
    path("Login-Admin/", AdminLoginViews.as_view(), name="AdminLogin"),

]
