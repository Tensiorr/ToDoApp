from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm, CustomLoginForm
from django.contrib import messages
from django.contrib.auth import login

def home_view(request):
    if request.user.is_authenticated:
        return redirect("tasks_list")
    return render(request, "home.html")

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        messages.success(self.request, "Rejestracja zakończona sukcesem. Możesz się teraz zalogować.")
        send_mail(
            'Witaj w ToDoApp!',
            'Dziękujemy za rejestrację.',
            settings.DEFAULT_FROM_EMAIL,
            [form.cleaned_data['email']],
            fail_silently=False,
        )
        return redirect("tasks_list")
    def form_invalid(self, form):
        messages.error(self.request, "Nie udało się zarejestrować. Popraw błędy w formularzu.")
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("tasks_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Zalogowano pomyślnie.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Nieprawidłowy login lub hasło.")
        return super().form_invalid(form)
