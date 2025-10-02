from django.http import Http404
from django.contrib.auth import get_user_model 
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .constants import POSTS_PER_PAGE 
from .forms import PostForm, UserEditForm, CommentForm
from .models import Category, Post, Comment
from .utils import _get_base_queryset, get_paginated_posts

# from django.views.decorators.http import require_POST


def index(request):
    qs = _get_base_queryset()
    page_obj = get_paginated_posts(request, qs, POSTS_PER_PAGE)
    context = {
        "page_obj": page_obj,
        "post_list": qs,
    }
    return render(request, "blog/index.html", context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, 
                                 slug=category_slug, 
                                 is_published=True)

    qs = _get_base_queryset().filter(category=category)
    
    page_obj = get_paginated_posts(request, qs, POSTS_PER_PAGE)
    context = {
        "category": category, 
        "page_obj": page_obj,
    }
    return render(request, "blog/category.html", context)


def profile(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    
    is_owner = request.user.is_authenticated and request.user == author
    if is_owner:
        qs = (Post.objects
          .filter(author=author)
          .select_related("author", "category", "location")
          .annotate(comment_count=Count('comments'))
          .order_by("-pub_date"))
    else:
        qs = _get_base_queryset().filter(author=author)

    page_obj = get_paginated_posts(request, qs, POSTS_PER_PAGE)
    context = {
        "author": author,
        "profile": author,
        "page_obj": page_obj,
        "is_owner": is_owner,
    }
    return render(request, "blog/profile.html", context)


# @login_required
# def edit_profile(request):
#     form = UserEditForm(request.POST or None, instance=request.user)
#     if form.is_valid():
#         form.save()
#         return redirect("blog:profile", request.user.username)

#     contex = {
#         "form": form,
#     }
#     return render(request, "blog/user.html", contex)
# #  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# Это другая версия edit_profile, тут добавлена проверка, что юзер
# не может редактировать чужой профиль. 
# Только она безсмысленна ведь проверка есть в шаблонах...
@login_required
def edit_profile(request):
    User = get_user_model()
    user_obj = get_object_or_404(User, username=request.user.username)

    # Нельзя редактировать чужой профиль
    if user_obj != request.user:
        return redirect("blog:profile", username=user_obj.username)

    form = UserEditForm(request.POST or None, instance=user_obj)
    if form.is_valid():
        form.save()
        return redirect("blog:profile", username=user_obj.username)

    return render(request, "blog/user.html", {"form": form})




def post_detail(request, post_id):
    # Добавить количество комментариев к посту
    # Отбор комментариев берем по модели комментариев (сейчас из поста)
    # Создание формы не понятно
    post = get_object_or_404(
        Post.objects
        .filter(
            id=post_id,
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True)
        .select_related("author", "category", "location")
    )
    comments = post.comments.select_related("author").order_by("created_at")
    form = CommentForm() if request.user.is_authenticated else None
    context = {
        "post": post, 
        "form": form, 
        "comments": comments
    }
    return render(request, "blog/detail.html", context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:profile", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "blog/create.html", {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post_id)
    else:
        form = PostForm(instance=post)

    context = {
        "form": form,
    }
    return render(request, "blog/create.html", context)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(
        Post.objects.filter(
            id=post_id,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        ).select_related("author", "category", "location")
    )
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)

    if request.method == "POST":
        author_username = post.author.username
        post.delete()
        return redirect("blog:profile", author_username)

    context = {
        "post": post,
        "is_delete": True
    }
    # подтверждение удаления — переиспользуем шаблон создания поста
    return render(request, "blog/create.html", context)


# @login_required
# def add_comment(request, post_id):
#     # 404, если пост не существует/не опубликован/категория скрыта/дата из будущего
#     post = get_object_or_404(
#         Post.objects.select_related("author", "category").filter(
#             is_published=True,
#             pub_date__lte=timezone.now(),
#             category__is_published=True,
#         ),
#         id=post_id, # ДОБАВИТЬ ЭТОТ ФИЛЬТР, ИНАЧЕ НЕ РАБОТАЕТ get_object_or_404
#     )

#     # 2) Разрешаем только POST. Остальные методы — обратно на страницу поста
#     if request.method != "POST":
#         return redirect("blog:post_detail", post_id=post.id)
    
#     form = CommentForm(request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.author = request.user   # привязываем автора
#         comment.post = post             # и пост
#         comment.save()
#         # redirect на страницу поста, где теперь будет новый комментарий
#         return redirect("blog:post_detail", post_id=post.id)

#     # Невалидную форму показываем на странице поста со статусом 200
#     comments = post.comments.select_related("author")
#     return render(
#         request,
#         "blog/detail.html",
#         {"post": post, "form": form, "comments": comments},
#     )
    
    
# # @login_required
# # def edit_comment(request, post_id, comment_id):
# #     post = get_object_or_404(
# #         Post.objects.filter(
# #             id=post_id,
# #             pub_date__lte=timezone.now(),
# #             category__is_published=True,
# #         )
# #     )
# #     comment = get_object_or_404(Comment.objects.select_related("author", "post"),
# #                                 id=comment_id, post=post)
    
# #     if comment.author != request.user:
# #         # править может только автор
# #         return redirect("blog:post_detail", post_id=post.id)
   
# #     form = CommentForm(request.POST or None, instance=comment)
# #     if request.method == "POST" and form.is_valid():
# #         form.save()
# #         return redirect("blog:post_detail", post_id=post.id)
# #     # можно отрендерить ту же страницу поста с формой редактирования,
# #     # но проще — отдельный небольшой шаблон
# #     return render(
# #         request,
# #         "blog/comment.html",
# #         {"form": form, "post": post, "comment": comment},
# #     )

# @login_required
# def edit_comment(request, post_id, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id, post_id=post_id, author=request.user)
#     form = CommentForm(request.POST or None, instance=comment)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return redirect("blog:post_detail", post_id=post_id)
#     return render(request, "blog/comment.html", {"form": form, "post": comment.post, "comment": comment})


# # @login_required
# # def delete_comment(request, post_id, comment_id):
# #     """Удаляет комментарий только его автору. Остальных — на просмотр поста."""
# #     post = get_object_or_404(
# #         Post.objects.filter(
# #             id=post_id,
# #             pub_date__lte=timezone.now(),
# #             category__is_published=True,
# #         )
# #     )
# #     comment = get_object_or_404(Comment, id=comment_id, post=post)

# #     if comment.author != request.user:
# #         return redirect("blog:post_detail", post_id=post.id)

# #     if request.method == "POST":
# #         comment.delete()
# #         return redirect("blog:post_detail", post_id=post.id)

# #     # подтверждение удаления — переиспользуем шаблон комментария
# #     return render(
# #         request,
# #         "blog/comment.html",
# #         {"post": post, "comment": comment, "is_delete": True},
# #     )


# @login_required
# def delete_comment(request, post_id, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id, post_id=post_id, author=request.user)
#     if request.method == "POST":
#         comment.delete()
#         return redirect("blog:post_detail", post_id=post_id)
#     return render(request, "blog/comment.html", {"post": comment.post, "comment": comment, "delete_mode": True})



# @login_required
# def add_comment(request, post_id):
#     post = get_object_or_404(
#         Post.objects.select_related("author", "category", "location"),
#         id=post_id
#     )
    
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#             return redirect("blog:post_detail", post_id=post.id)
#     else:
#         form = CommentForm() # для GET — пустая форма

#     # Не валидно: просто показать ту же страницу поста с формой и ошибками.
#     # (Это на прохождение текущих тестов не влияет, но поведение правильное.)
#     comments = post.comments.select_related("author").order_by("created_at")

#     context = {
#         "post": post, 
#         "form": form, 
#         "comments": comments,
#     }
#     return render(request, "blog/detail.html", context)


from django.http import Http404
from django.views.decorators.http import require_POST

@login_required
@require_POST
def add_comment(request, post_id):
    # жёстко проверяем существование поста в базе
    try:
        post = Post.objects.select_related("author", "category", "location").get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        # 👇 тесты ждут именно редирект на detail, а не рендер
        return redirect("blog:post_detail", post_id=post.id)

    # если форма невалидна — остаёмся на detail
    comments = post.comments.select_related("author").order_by("created_at")
    context = {"post": post, "form": form, "comments": comments}
    return render(request, "blog/detail.html", context, status=200)



@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(
        Comment,
        pk=comment_id, post=post)
    if comment.author != request.user:
        raise Http404
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post.id)
    context = {
        "form": form, 
        "post": post, 
        "comment": comment
    }
    return render(request, "blog/comment.html", context)


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария."""
    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(
        Comment, pk=comment_id, post=post)
    if comment.author != request.user:
        raise Http404
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post.id)
    context = {
            "post": post, 
            "comment": comment,
        }
    return render(request, "blog/comment.html", context)
