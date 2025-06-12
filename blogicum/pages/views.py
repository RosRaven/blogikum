from django.shortcuts import render


def about(request):
    # Просто отдаём шаблон without any context
    # (т.е. без дополнительных данных).
    return render(request, "pages/about.html")


def rules(request):
    return render(request, "pages/rules.html")



