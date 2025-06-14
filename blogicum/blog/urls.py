from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # 1) Главная лента: список всех постов
    path("", 
         views.post_list, name="post_list"),      # раньше был index, но post_list понятнее
     # 2) Детали поста по его slug (не по ID)
     #    т.к. в модели вы определили get_absolute_url(slug=...)
    path("posts/<slug:slug>/", 
         views.post_detail, name="post_detail"),
     # 3) Лента по конкретной категории (slug категории)
    path("category/<slug:category_slug>/", 
         views.category_posts, name="category_posts"),
]
