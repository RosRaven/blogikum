from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def index(request):
    now = timezone.now()
    posts = (Post.objects
             .filter(is_published=True,
                     pub_date__lte=now,
                     category__is_published=True)
             .order_by("-pub_date")[:5])
    return render(request, "blog/index.html", {"posts": posts})


def post_detail(request, slug):
    now = timezone.now()
    #  вернёт 404, если не найдёт запись.
    post = get_object_or_404(
        # Мы сразу фильтруем и по slug, и по флагам/датам — ничего «лишнего» не попадёт.
        Post.objects.filter(
            slug=slug,
            is_published=True,
            pub_date__lte=now,
            category__is_published=True,
        )
    )
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    now = timezone.now()
    # Сначала убедимся, что категория существует и опубликована
    category = get_object_or_404(
        Category.objects.filter(slug=category_slug, is_published=True)
    )
    # Затем получим её посты по тем же правилам, что и в index()
    posts = (
        Post.objects
             .filter(category=category,
                     is_published=True,
                     pub_date__lte=now,
                     )
             .order_by("-pub_date"))
    return render(
        request, 
        "blog/category.html", 
        {"posts": posts},
    )
