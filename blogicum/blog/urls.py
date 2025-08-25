from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
     path("", views.index, name="index"),
     path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
     path("category/<slug:category_slug>/", views.category_posts, name="category_posts"),
     path("profile/<str:username>/", views.profile, name="profile"),

     # создание
     path("posts/create/", views.post_create, name="create_post"),

     # РЕДАКТИРОВАНИЕ
     path("posts/<int:post_id>/edit/", views.post_edit, name="edit_post"),

     path("profile/edit/", views.edit_profile, name="edit_profile"),
]
