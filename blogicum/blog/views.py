from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .constants import POSTS_ON_MAIN
from .models import Post, Category

def _get_base_queryset():
    return Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
            ).order_by("-pub_date")


def index(request):
    post_list = _get_base_queryset()[:POSTS_ON_MAIN]
    return render(request, "blog/index.html", {"post_list": post_list})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects
            .filter(
                id=post_id,
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True)
            )
    
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects
            .filter(
                slug=category_slug, 
                is_published=True
                )
            )
    post_list = _get_base_queryset().filter(category=category)
    
    return render(
        request, 
        "blog/category.html", 
        {
            "category": category,
            "post_list": post_list
        }
    )
