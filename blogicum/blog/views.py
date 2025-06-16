from django.shortcuts import render


def index(request):
    """
    1) Главная страница: отдаём все посты.
    render(request, template, context)
    — оборачивает шаблон blog/index.html в HttpResponse,
      передавая ему context = {'posts': posts}.
    """
    ordered_posts = sorted(posts, key=lambda p: p["id"], reverse=True)
    # сортируем по id, чтобы новые были первыми
    return render(request, "blog/index.html", {"posts": ordered_posts})


def post_detail(request, post_id):
    """
    2) Детальный просмотр одного поста:
    Параметр `id` приходит из URL (конвертер <int:id>).
    next(...) находит первый словарь в posts с таким id,
    либо None, если не найден.
    """
    # ищем словарь с нужным id
    post = next((p for p in posts if p["id"] == post_id), None)
    if post is None:
        # если не нашли, возвращаем 404
        return render(request, "404.html", status=404)

    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    """
    Показывает страницу «Публикации в категории X».
    Пока без списка самих постов, только название категории из URL.
    """
    return render(
        request,
        "blog/category.html",
        {
            "category_slug": category_slug,
        },
    )


# def category_posts(request, category_slug):
# """
# 3) Публикации по категории:
# Параметр `category_slug` — строка из URL (<slug:category_slug>).
# Фильтруем все p['category'] == category_slug
# и отдаём шаблону blog/category.html два ключа:
#   - 'category_slug' (для заголовка)
#   - 'posts' — список отфильтрованных постов.
# """
# filtered = [post for post in posts if post['category'] == category_slug]
# return render(request, 'blog/category.html', {'category_slug': category_slug, 'posts': filtered})
