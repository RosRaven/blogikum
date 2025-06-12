from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    # 1) Главная лента
    path("", 
         views.index, name="index"),
    # 2) Детали поста по ID
    path("posts/<int:post_id>/", 
         views.post_detail, name="post_detail"),
    # 3) Публикации по категории
    path("category/<slug:category_slug>/", 
         views.category_posts, name="category_posts"),
]
