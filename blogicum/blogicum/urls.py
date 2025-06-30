"""
URL configuration for blogicum project.

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
from django.contrib.auth.views import LogoutView
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

from blog.views import SignUpView, custom_logout

urlpatterns = [
    path("admin/", admin.site.urls),
    # сюда попадают /accounts/login/, /accounts/logout/, /accounts/password_change/ и т. д.
    
    # регистрация (если ты её сделаешь отдельным CBV)
    path('accounts/signup/', SignUpView.as_view(), name='signup'),

    # наш упрощённый logout
    path("accounts/logout/", custom_logout, name="logout"),

    path("accounts/", include("django.contrib.auth.urls")),
    
    path(
        "accounts/profile/",
        RedirectView.as_view(url=reverse_lazy('blog:index')),
        name="profile"),

    # главная лента из приложения blog
    path("", include("blog.urls", namespace="blog")),
    # статические страницы из приложения pages
    path("pages/", include("pages.urls", namespace="pages")),
    ]
