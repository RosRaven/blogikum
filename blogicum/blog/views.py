from django.contrib.auth import get_user_model # возвращает активную модель пользователя
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator ###
from django.http import HttpResponse # нужен только для заглушки — когда сделаем форму, этот импорт тоже можно убрать.
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .constants import POSTS_ON_MAIN, POSTS_PER_PAGE 
from .models import Post, Category
from .utils import _get_base_queryset

@login_required # Это защита - страница добавления публикации доступна только авторизованным
def post_create(request):
    # заглушка; заменить реализацией позже
    return HttpResponse(
        "Форма создания поста будет реализована позже.", 
        status=501)


def profile(request, username):
    # 1) находим пользователя по username или отдаём 404
    author = get_object_or_404(get_user_model(), username=username)

    # 2) собираем queryset постов этого автора (не «из будущего»)
    posts = (Post.objects
             .select_related("author", "category", "location")
             .filter(author=author, pub_date__lte=timezone.now())
             .order_by("-pub_date"))

    # 3) если у модели есть флаг публикации — учитываем его
    if any(f.name == "is_published" for f in Post._meta.fields):
        posts = posts.filter(is_published=True)

    # 4) пагинация
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    # 5) контекст для шаблона
    context = {
        "author": author,         # привычное имя для шаблонов
        "profile": author,        # иногда тесты ждут именно 'profile'
        "page_obj": page_obj,     # данные и навигация пагинатора
        "is_owner": request.user.is_authenticated and request.user == author,
    }
    return render(request, "blog/profile.html", context)


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


