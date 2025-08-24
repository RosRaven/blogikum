from django.urls import path

from . import views


app_name = "pages"

urlpatterns = [
    # 4) О проекте
    path("about/", views.about, name="about"),
    # 5) Наши правила
    path("rules/", views.rules, name="rules"),
    
    # временная заглушка для проверки ошибки 500
    path("boom/", views.boom, name="boom"),
]
