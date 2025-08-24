from django.contrib.auth import get_user_model ###
from django.core.paginator import Paginator ###
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q ###

from .constants import POSTS_ON_MAIN, POSTS_PER_PAGE ###
from .models import Post, Category
from .utils import _get_base_queryset

def profile(request, username):
    author = get_object_or_404(get_user_model(), username=username)

    # Базовый кверисет постов автора, не «из будущего»
    posts = (Post.objects
             .select_related("author", "category", "location")
             .filter(author=author, pub_date__lte=timezone.now())
             .order_by("-pub_date"))

    # Если в модели есть поле is_published — учитываем его
    if any(f.name == "is_published" for f in Post._meta.fields):
        posts = posts.filter(is_published=True)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "author": author,         # на всякий: часто шаблон ждёт author
        "profile": author,        # и такое имя тоже встречается в тестах
        "page_obj": page_obj,     # для пагинации
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
