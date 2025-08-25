# возвращает активную модель пользователя
from django.contrib.auth import get_user_model 
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .constants import POSTS_ON_MAIN, POSTS_PER_PAGE 
from .models import Post, Category
from .utils import _get_base_queryset, get_paginated_posts
from .forms import PostForm


# Это защита - страница добавления публикации доступна только авторизованным
@login_required
def post_create(request):
    """
    Создание новой публикации (доступно только авторизованным).
    После успешной валидации — редирект на профиль автора.
    """
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # автор — текущий пользователь
            post.save()
            # form.save_m2m() тут не нужен (у нас нет M2M), но не мешает.
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "blog/create.html", {"form": form})


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
    """
    Профиль пользователя.
    Владельцу профиля показываем все его записи (включая будущие и снятые),
    остальным — только опубликованные и не «из будущего».
    """

    # 1) находим пользователя по username или отдаём 404
    author = get_object_or_404(get_user_model(), username=username)
    is_owner = request.user.is_authenticated and request.user == author

    # 2) 
    if is_owner:
        # Все посты автора, без ограничений по публикации/дате
        qs = (Post.objects
          .filter(author=author)
          .select_related("author", "category", "location")
          .order_by("-pub_date"))
    else:
        # собираем queryset постов этого автора (не «из будущего»)
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
        "is_owner": is_owner,     # это мой профиль?
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
