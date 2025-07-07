from .views import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import re


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Login:",
        help_text="",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        required=True,
        label="Email:",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Hasło:",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="",
    )
    password2 = forms.CharField(
        label="Powtórz hasło:",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="",
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
        help_texts = {
            "username": "",
            "password1": "",
            "password2": "",
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < 6:
            raise ValidationError("Login musi mieć minimum 6 znaków.")
        if not re.match("^[a-zA-Z0-9_]+$", username):
            raise ValidationError("Login może zawierać tylko litery, cyfry i _.")
        return username

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 6:
            raise ValidationError("Hasło musi mieć minimum 6 znaków.")
        if not re.search(r"\d", password):
            raise ValidationError("Hasło musi zawierać co najmniej jedną cyfrę.")
        if not re.search(r"[a-zA-Z]", password):
            raise ValidationError("Hasło musi zawierać litery.")
        return password


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Login:", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Hasło:", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
