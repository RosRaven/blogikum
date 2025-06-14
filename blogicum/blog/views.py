from django.shortcuts import render, get_object_or_404
from .models import Post, Category


def post_list(request):
    """
    1) Главная лента: список всех постов из БД, 
    отсортированных согласно Meta.ordering.
    """
    posts = Post.objects.all()
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, slug):
    """
    2) Детальный просмотр одного поста по его slug.
    Если не найден — 404.
    """
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post_detail.html", {"post": post})


def category_posts(request, category_slug):
    """
    3) Лента по категории: находим Category по slug, 
    берём все связанные посты и передаём в шаблон.
    """
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    return render(
        request,
        "blog/category.html",
        {
            "category": category,
            "posts": posts,
        },
    )
