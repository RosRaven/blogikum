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

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path

from pages import views as pages_views # временно для заглушки


urlpatterns = [
    path("admin/", admin.site.urls),

    # главная лента из приложения blog
    path("", include("blog.urls", namespace="blog")),
    # статические страницы из приложения pages
    path("pages/", include("pages.urls", namespace="pages")),

    # даст name='login' и пр.
    # # Стандартные пути аутентификации: login/logout/password*
    path("auth/", include("django.contrib.auth.urls")),

    # Регистрация (по заданию)
    path("auth/registration/", pages_views.RegistrationView.as_view(), name="registration"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"
