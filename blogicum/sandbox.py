import os
import django

# указываем, где settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogicum.settings")
django.setup()



# def test_models():
#     from blog.models import Category, Post
#     # 1) Категории без description (blank=True, null=False)
#     c = Category.objects.create(name="Тест", slug="test")
#     print("Category.description:", repr(c.description))  # ""  

#     # 2) Посты без published_at (blank=True, null=True)
#     p = Post.objects.create(
#         title="Заголовок", slug="zagl", content="...", category=c
#     )
#     print("Post.published_at:", p.published_at)  # None


def test_models():
    from blog.models import Category, Post

    # Чистим только наши тестовые slugs
    Post.objects.filter(slug__in=["p-default", "p-pub"]).delete()
    Category.objects.filter(slug="choices-test").delete()

    # Создаём категорию
    c, created_c = Category.objects.get_or_create(
        slug="choices-test",
        defaults={"name": "ЧойсСпринт"}
    )
    print("Category created?", created_c)

    # Создаём посты
    p1, created_p1 = Post.objects.get_or_create(
        slug="p-default",
        defaults={
            "title": "Пост по умолчанию",
            "content": "...",
            "category": c,
        }
    )
    print("p1.status (default):", p1.status, "; created?", created_p1)

    p2, created_p2 = Post.objects.get_or_create(
        slug="p-pub",
        defaults={
            "title": "Пост опубликованный",
            "content": "...",
            "category": c,
            "status": "published",
        }
    )
    print("p2.status (explicit):", p2.status, "; created?", created_p2)

    print("Posts in category:", list(c.posts.all()))

if __name__ == "__main__":
    test_models()


if __name__ == "__main__":
    # test_models()
    test_models()  # вызовем тестовую функцию для проверки моделей
