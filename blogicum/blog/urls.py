from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
     path("", 
          views.index, 
          name="index"),
     # Заменил int на slug, чтобы использовать слаг в URL
     path("posts/<slug:slug>/", 
          views.post_detail, 
          name="post_detail"),
     path("category/<slug:category_slug>/", 
          views.category_posts, 
          name="category_posts"),
]
