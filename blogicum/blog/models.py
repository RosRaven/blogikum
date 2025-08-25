# Ссылаемся на модель пользователя, чтобы использовать её в ForeignKey.
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE, SET_NULL
# делает метки и подсказки переводимыми.
from django.utils.translation import gettext_lazy as _  

from .constants import TITLE_MAX_LENGTH, NAME_MAX_LENGTH, TITLE_REPL_MAX_LENGTH, NAME_REPL_MAX_LENGTH

# from django.urls import reverse
# Получаем модель пользователя, которая используется в проекте.
# Это позволяет использовать кастомную модель пользователя, если она есть.

User = get_user_model()

class TimestampedModel(models.Model):
    """
    Абстрактная модель: добавляет флаги публикации и отображения на главной.
    """
    # флажок, можно скрыть категорию.
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Опубликовано"),
        help_text=_("Снимите галочку, чтобы скрыть публикацию.")
    )
    # дата-время создания записи, проставляется автоматически.
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Добавлено")
    )
    
    class Meta:
        # Эта модель не будет создана в базе данных, но её поля будут доступны в дочерних моделях.
        abstract = True


class Category(TimestampedModel):
    """
    Модель категории для постов в блоге.
    """
    # уникальное название
    title = models.CharField(
        verbose_name=_("Заголовок"),
        max_length=TITLE_MAX_LENGTH,
        help_text=_("Максимальная длина строки — %(length)d символов", 
                    ) % {"length": TITLE_MAX_LENGTH}
    )
    # произвольный текст, без ограничения длины, описывает категорию.
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Краткое описание категории")
    )
    # URL-дружественный идентификатор (slug), должен быть уникальным.
    slug = models.SlugField(
        verbose_name=_("Идентификатор"),
        unique=True,
        help_text=_("Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.")
    )

    class Meta:
        # переводимые названия модели в единственном и множественном числе.
        verbose_name = _("категория")
        verbose_name_plural = _("Категории")
        
    def __str__(self):
        return self.title[:TITLE_REPL_MAX_LENGTH]


class Location(TimestampedModel):
    """
    Модель локации для постов в блоге.
    """
    # название локации.
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name=_("Название места"),
        help_text=_("Максимальная длина строки — %(length)d символов"
                    ) % {"length": NAME_MAX_LENGTH}
    )

    class Meta:
        # переводы названий модели в единственном и множественном числе.
        verbose_name = _("местоположение")
        verbose_name_plural = _("Местоположения")

    def __str__(self):
        return self.name[:NAME_REPL_MAX_LENGTH]


class Post(TimestampedModel):
    """Модель поста в блоге."""
    # заголовок поста
    title = models.CharField(
        verbose_name=_("Заголовок"),
        max_length=TITLE_MAX_LENGTH,
        help_text=_("Максимальная длина строки — %(length)d символов"
                    ) % {"length": TITLE_MAX_LENGTH}
    )
    # содержание  поста
    text = models.TextField(
        verbose_name=_("Текст"),
        )
    # дата публикации (может быть в будущем для отложенных постов)
    pub_date = models.DateTimeField(
        verbose_name=_("Дата и время публикации"),
        help_text=_("Если установить дату и время в будущем — можно делать отложенные публикации.")
    )
    #  связь с пользователем, CASCADE убирает пост при удалении автора.
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name=_("Автор публикации")
    )
        # SET_NULL, чтобы при удалении локации поле просто обнулялось, а пост сохранялся.
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=SET_NULL,
        verbose_name=_("Местоположение")
    )
    # CASCADE, но null=True (хотя тесты требуют именно null=True, blank=False).
    category = models.ForeignKey(
        Category,
        null=True,
        blank=False,
        on_delete=SET_NULL,
        verbose_name=_("Категория")
    )

    image = models.ImageField(
        upload_to='posts/',
        verbose_name=_("Изображение"),
        help_text=_("Загрузите изображение для публикации."),
        blank=True, # чтобы поле было необязательным
    )

    class Meta:
        # переводимые названия модели в единственном и множественном числе.
        verbose_name = _("публикация")
        verbose_name_plural = _("Публикации")

    def __str__(self):
        return self.title[:TITLE_REPL_MAX_LENGTH]

