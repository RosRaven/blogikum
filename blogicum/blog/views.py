from django.shortcuts import render, get_object_or_404, redirect
# render позволяет отдать HTML-шаблон + контекст, redirect — перенаправить после успешного сохранения.
from django.utils import timezone

from .constants import POSTS_ON_MAIN
from .forms import PostForm
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


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # request.FILES для будущих полей файлов
        # запускает всю валидацию: поля + методы clean_….
        if form.is_valid():
            # создаёт объект Post, но не сохраняет в БД сразу — чтобы мы успели что-то до-настроить.
            post = form.save(commit=False)
            # проставляем автора (твоё приложение раньше не включало это поле в форму).
            post.author = request.user
            # сохраняем в БД.
            post.save()
            # после успешного создания отправляем пользователя на страницу с детальным просмотром.
            return redirect('post_detail', pk=post.pk)
    else:
        # Если это не POST (т. е. GET, когда пользователь впервые открыл страницу), создаём пустую форму
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})
