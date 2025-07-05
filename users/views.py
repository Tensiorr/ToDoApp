# from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from django.contrib.auth.views import LoginView, LogoutView


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class CustomLoginView(LoginView):
    template_name = "login.html"
