from django.contrib import admin
from django.urls import path, include
from .views import UserRegistrationView, RegisteredUsersView

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name="register-users"),
    path('users', RegisteredUsersView.as_view()),
]