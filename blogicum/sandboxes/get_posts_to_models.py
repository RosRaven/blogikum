import os
import django
from datetime import datetime

from datetime import date

RUS_MONTHS = {
    "января":   1, "февраля":  2, "марта":    3,
    "апреля":   4, "мая":      5, "июня":     6,
    "июля":     7, "августа":  8, "сентября": 9,
    "октября":  10, "ноября":  11, "декабря":  12,
}

import locale

# 1) Настройка Django
# Указываем, где лежат настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogicum.settings")
django.setup()

# 2) Ваши исходные данные — raw_posts **должен быть здесь**, до любых print
raw_posts = [
    {
        "id": 0,
        "location": "Остров отчаянья",
        "date": "30 сентября 1659 года",
        "category": "travel",
        "text": """Наш корабль, застигнутый в открытом море
                страшным штормом, потерпел крушение.
                Весь экипаж, кроме меня, утонул; я же,
                несчастный Робинзон Крузо, был выброшен
                полумёртвым на берег этого проклятого острова,
                который назвал островом Отчаяния.""",
    },
    {
        "id": 1,
        "location": "Остров отчаянья",
        "date": "1 октября 1659 года",
        "category": "not-my-day",
        "text": """Проснувшись поутру, я увидел, что наш корабль сняло
                с мели приливом и пригнало гораздо ближе к берегу.
                Это подало мне надежду, что, когда ветер стихнет,
                мне удастся добраться до корабля и запастись едой и
                другими необходимыми вещами. Я немного приободрился,
                хотя печаль о погибших товарищах не покидала меня.
                Мне всё думалось, что, останься мы на корабле, мы
                непременно спаслись бы. Теперь из его обломков мы могли бы
                построить баркас, на котором и выбрались бы из этого
                гиблого места.""",
    },
    {
        "id": 2,
        "location": "Остров отчаянья",
        "date": "25 октября 1659 года",
        "category": "not-my-day",
        "text": """Всю ночь и весь день шёл дождь и дул сильный
                порывистый ветер. 25 октября.  Корабль за ночь разбило
                в щепки; на том месте, где он стоял, торчат какие-то
                жалкие обломки,  да и те видны только во время отлива.
                Весь этот день я хлопотал  около вещей: укрывал и
                укутывал их, чтобы не испортились от дождя.""",
    },
]

from blog.models import Category, Post

# Опционально: для парсинга русских месяцев
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

# 3) Отладочные принты
print("▶ sandbox.py загружен")
print("raw_posts length:", len(raw_posts))

# Функция для импорта постов из raw_posts в базу данных
def import_posts():
    print("▶ import_posts() запущен")
    # теперь Category и Post доступны

    # очистка
    # Post.objects.filter(slug__startswith="imported-").delete()
    Post.objects.all().delete()
    # Category.objects.filter(slug__in={"travel", "not-my-day"}).delete()
    Category.objects.all().delete()

    for d in raw_posts:
        cat, _ = Category.objects.get_or_create(
            slug=d["category"],
            defaults={"name": d["category"].replace("-", " ").capitalize()}
        )
        raw = d["date"]
        parts = raw.replace(" года", "").split()  # ["30", "сентября", "1659"]
        try:
            day = int(parts[0])
            month = RUS_MONTHS[parts[1].lower()]
            year = int(parts[2])
            parsed = date(year, month, day)
        except ValueError:
            parsed = None

        post = Post.objects.create(
            title=f"Запись #{d['id']} — {raw}",
            slug=f"imported-{d['id']}",
            content=d["text"],
            category=cat,
            location=d["location"],
            event_date_raw=raw,
            event_date=parsed,
        )
        print(f"Imported {post.slug}: raw='{raw}', parsed={parsed}")

# 5) Точка входа
if __name__ == "__main__":
    import_posts()