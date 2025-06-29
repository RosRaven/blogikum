from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .constants import POSTS_ON_MAIN
from .models import Post, Category

def get_posts(type_request, category=None):
    if type_request == "main":
        post_list = (Post.objects
                .filter(is_published=True,
                        pub_date__lte=timezone.now(),
                        category__is_published=True)
                .order_by("-pub_date")[:POSTS_ON_MAIN]
                )
    elif type_request == "category":
        post_list = (Post.objects
                .filter(is_published=True,
                        pub_date__lte=timezone.now(),
                        category=category
                        )
                .order_by("-pub_date")
                )

    return post_list


def index(request):
    post_list = get_posts("main")

    # post_list = (Post.objects
    #          .filter(is_published=True,
    #                  pub_date__lte=timezone.now(),
    #                  category__is_published=True)
    #          .order_by("-pub_date")[:POSTS_ON_MAIN]
    #          )
    return render(request, "blog/index.html", {"post_list": post_list})


def post_detail(request, post_id):
    #  вернёт 404, если не найдёт запись.
    post = get_object_or_404(
        # ищем по id и сразу проверяем флаги и дату
        Post.objects
            .filter(
                id=post_id,
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True)
            )
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    # 1) Достаём категорию или 404, если её нет или она не опубликована
    category = get_object_or_404(
        Category.objects
            .filter(
                slug=category_slug, 
                is_published=True
                )
            )

    # 2) Формируем QuerySet её постов по тем же правилам, что и на главной
    post_list = get_posts(type_request="category", category=category)
    
    # post_list = (
    #     Post.objects
    #         .filter(category=category,
    #                 is_published=True,
    #                 pub_date__lte=timezone.now(),
    #                 )
    #         .order_by("-pub_date")
    #         )
    
    # 3) Отдаём и категорию, и список в ключах именно "category" и "post_list"
    return render(
        request, 
        "blog/category.html", 
        {
            "category": category,
            "post_list": post_list
        }
    )
