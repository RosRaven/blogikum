# import os
# import django

# # указываем, где settings
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogicum.settings")
# django.setup()



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








# from blog.models import Post, Category

# # Проверяем метаданные поля status у Post
# field_status = Post._meta.get_field("status")
# print("Post.status verbose_name:", field_status.verbose_name)
# print("Post.status help_text   :", field_status.help_text)

# # Проверяем метаданные поля description у Category
# field_desc = Category._meta.get_field("description")
# print("Category.description verbose_name:", field_desc.verbose_name)
# print("Category.description help_text   :", field_desc.help_text)





# import os
# import django
# from datetime import datetime

# from datetime import date

# RUS_MONTHS = {
#     "января":   1, "февраля":  2, "марта":    3,
#     "апреля":   4, "мая":      5, "июня":     6,
#     "июля":     7, "августа":  8, "сентября": 9,
#     "октября":  10, "ноября":  11, "декабря":  12,
# }

# import locale

# # 1) Настройка Django
# # Указываем, где лежат настройки Django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogicum.settings")
# django.setup()

# # 2) Ваши исходные данные — raw_posts **должен быть здесь**, до любых print
# raw_posts = [
#     {
#         "id": 0,
#         "location": "Остров отчаянья",
#         "date": "30 сентября 1659 года",
#         "category": "travel",
#         "text": """Наш корабль, застигнутый в открытом море
#                 страшным штормом, потерпел крушение.
#                 Весь экипаж, кроме меня, утонул; я же,
#                 несчастный Робинзон Крузо, был выброшен
#                 полумёртвым на берег этого проклятого острова,
#                 который назвал островом Отчаяния.""",
#     },
#     {
#         "id": 1,
#         "location": "Остров отчаянья",
#         "date": "1 октября 1659 года",
#         "category": "not-my-day",
#         "text": """Проснувшись поутру, я увидел, что наш корабль сняло
#                 с мели приливом и пригнало гораздо ближе к берегу.
#                 Это подало мне надежду, что, когда ветер стихнет,
#                 мне удастся добраться до корабля и запастись едой и
#                 другими необходимыми вещами. Я немного приободрился,
#                 хотя печаль о погибших товарищах не покидала меня.
#                 Мне всё думалось, что, останься мы на корабле, мы
#                 непременно спаслись бы. Теперь из его обломков мы могли бы
#                 построить баркас, на котором и выбрались бы из этого
#                 гиблого места.""",
#     },
#     {
#         "id": 2,
#         "location": "Остров отчаянья",
#         "date": "25 октября 1659 года",
#         "category": "not-my-day",
#         "text": """Всю ночь и весь день шёл дождь и дул сильный
#                 порывистый ветер. 25 октября.  Корабль за ночь разбило
#                 в щепки; на том месте, где он стоял, торчат какие-то
#                 жалкие обломки,  да и те видны только во время отлива.
#                 Весь этот день я хлопотал  около вещей: укрывал и
#                 укутывал их, чтобы не испортились от дождя.""",
#     },
# ]

# from blog.models import Category, Post

# # Опционально: для парсинга русских месяцев
# locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

# # 3) Отладочные принты
# print("▶ sandbox.py загружен")
# print("raw_posts length:", len(raw_posts))

# # Функция для импорта постов из raw_posts в базу данных
# def import_posts():
#     print("▶ import_posts() запущен")
#     # теперь Category и Post доступны

#     # очистка
#     # Post.objects.filter(slug__startswith="imported-").delete()
#     Post.objects.all().delete()
#     # Category.objects.filter(slug__in={"travel", "not-my-day"}).delete()
#     Category.objects.all().delete()

#     for d in raw_posts:
#         cat, _ = Category.objects.get_or_create(
#             slug=d["category"],
#             defaults={"name": d["category"].replace("-", " ").capitalize()}
#         )
#         raw = d["date"]
#         parts = raw.replace(" года", "").split()  # ["30", "сентября", "1659"]
#         try:
#             day = int(parts[0])
#             month = RUS_MONTHS[parts[1].lower()]
#             year = int(parts[2])
#             parsed = date(year, month, day)
#         except ValueError:
#             parsed = None

#         post = Post.objects.create(
#             title=f"Запись #{d['id']} — {raw}",
#             slug=f"imported-{d['id']}",
#             content=d["text"],
#             category=cat,
#             location=d["location"],
#             event_date_raw=raw,
#             event_date=parsed,
#         )
#         print(f"Imported {post.slug}: raw='{raw}', parsed={parsed}")

# # 5) Точка входа
# if __name__ == "__main__":
#     import_posts()
