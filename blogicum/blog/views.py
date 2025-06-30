from django.contrib.auth.decorators import login_required
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


# не даёт анонимным пользователям попасть на страницу создания.
@login_required
def post_create(request):
    # 1) При GET просто показываем пустую форму
    if request.method == "GET":
        form = PostForm()
        return render(request, 'blog/post_form.html', {"form": form})

    # 2) При POST обрабатываем отправленные данные
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # request.FILES для будущих полей файлов
        # запускает все проверки (clean_… и встроенные).
        if not form.is_valid():
            # Если форма не прошла валидацию, снова рендерим шаблон с ошибками
            return render(request, 'blog/post_form.html', {'form': form})

    # 3) Сохраняем объект, но ещё не в БД, чтобы проставить автора
    post = form.save(commit=False)
    post.author = request.user
    post.save()

    # 4) После успешного сохранения — редирект на детальный просмотр
    return redirect('blog:post_detail', post_id=post.pk)
