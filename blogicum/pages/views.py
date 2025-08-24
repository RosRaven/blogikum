from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render


def about(request):
    # Просто отдаём шаблон without any context
    # (т.е. без дополнительных данных).
    return render(request, "pages/about.html")


def rules(request):
    return render(request, "pages/rules.html")


def page_not_found(request, exception):
    return render(request, "pages/404.html", status=404)


def server_error(request):
    return render(request, "pages/500.html", status=500)


def csrf_failure(request, reason=""):
    return render(request, "pages/403csrf.html", {"reason": reason}, status=403)


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/registration_form.html"
    
    # после регистрации переходим на страницу входа
    success_url = reverse_lazy("login") # ← так ожидают чаще всего
