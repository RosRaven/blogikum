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


# def test_models():
#     from blog.models import Category, Post

#     # Чистим только наши тестовые slugs
#     Post.objects.filter(slug__in=["p-default", "p-pub"]).delete()
#     Category.objects.filter(slug="choices-test").delete()

#     # Создаём категорию
#     c, created_c = Category.objects.get_or_create(
#         slug="choices-test",
#         defaults={"name": "ЧойсСпринт"}
#     )
#     print("Category created?", created_c)

#     # Создаём посты
#     p1, created_p1 = Post.objects.get_or_create(
#         slug="p-default",
#         defaults={
#             "title": "Пост по умолчанию",
#             "content": "...",
#             "category": c,
#         }
#     )
#     print("p1.status (default):", p1.status, "; created?", created_p1)

#     p2, created_p2 = Post.objects.get_or_create(
#         slug="p-pub",
#         defaults={
#             "title": "Пост опубликованный",
#             "content": "...",
#             "category": c,
#             "status": "published",
#         }
#     )
#     print("p2.status (explicit):", p2.status, "; created?", created_p2)

#     print("Posts in category:", list(c.posts.all()))

# if __name__ == "__main__":
#     test_models()


# if __name__ == "__main__":
#     # test_models()
#     test_models()  # вызовем тестовую функцию для проверки моделей







# from django.db import models
# from blog.models import Post, Category

# # Получаем объект поля
# field = Post._meta.get_field("status")
# print("Post.status verbose_name:", field.verbose_name)
# print("Post.status help_text   :", field.help_text)

# field2 = Category._meta.get_field("description")
# print("Category.description verbose_name:", field2.verbose_name)
# print("Category.description help_text   :", field2.help_text)








from blog.models import Post, Category

# Проверяем метаданные поля status у Post
field_status = Post._meta.get_field("status")
print("Post.status verbose_name:", field_status.verbose_name)
print("Post.status help_text   :", field_status.help_text)

# Проверяем метаданные поля description у Category
field_desc = Category._meta.get_field("description")
print("Category.description verbose_name:", field_desc.verbose_name)
print("Category.description help_text   :", field_desc.help_text)
