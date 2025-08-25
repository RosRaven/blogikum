# возвращает активную модель пользователя
from django.contrib.auth import get_user_model 
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.utils import timezone

# нужен только для заглушки — когда сделаем форму, этот импорт тоже можно убрать.
from django.http import HttpResponse 

from .constants import POSTS_ON_MAIN, POSTS_PER_PAGE 
from .models import Post, Category
from .utils import _get_base_queryset, get_paginated_posts


@login_required # Это защита - страница добавления публикации доступна только авторизованным
def post_create(request):
    # заглушка; заменить реализацией позже
    return HttpResponse(
        "Форма создания поста будет реализована позже.", 
        status=501)


def index(request):
    qs = (_get_base_queryset()
          .select_related("author", "category", "location"))
    page_obj = get_paginated_posts(request, qs, POSTS_ON_MAIN)
    context = {
        "page_obj": page_obj,
        "post_list": qs,
    }
    return render(request, "blog/index.html", context)


def profile(request, username):
    # 1) находим пользователя по username или отдаём 404
    author = get_object_or_404(get_user_model(), username=username)

    # 2) собираем queryset постов этого автора (не «из будущего»)
    qs = (_get_base_queryset()
          .filter(author=author)
          .select_related("author", "category", "location"))

    # 4) пагинация
    page_obj = get_paginated_posts(request, qs, POSTS_PER_PAGE)

    # 5) контекст для шаблона
    context = {
        "author": author,         # привычное имя для шаблонов
        "profile": author,        # иногда тесты ждут именно 'profile'
        "page_obj": page_obj,     # данные и навигация пагинатора
        "post_list": page_obj,    # совместимость со старыми инклюдами
        "is_owner": request.user.is_authenticated and request.user == author,
    }
    return render(request, "blog/profile.html", context)


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
    qs = (_get_base_queryset()
          .filter(category=category)
          .select_related("author", "category", "location"))
    
    page_obj = get_paginated_posts(request, qs, POSTS_PER_PAGE)
    context = {"category": category, 
               "page_obj": page_obj, 
               "post_list": page_obj}
    return render(
        request, 
        "blog/category.html", 
        context)
