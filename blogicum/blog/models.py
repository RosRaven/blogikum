from django.db import models
from django.db.models import SET_NULL, CASCADE
# Ссылаемся на модель пользователя, чтобы использовать её в ForeignKey.
from django.contrib.auth import get_user_model 
from django.utils.translation import gettext_lazy as _ # делает метки и подсказки переводимыми.
# from django.urls import reverse
# Получаем модель пользователя, которая используется в проекте.
# Это позволяет использовать кастомную модель пользователя, если она есть.

User = get_user_model()


class Category(models.Model):
    """
    Модель категории для постов в блоге.
    """
    # уникальное название
    title = models.CharField(
        verbose_name=_("Заголовок"),
        max_length=256,
        help_text=_("Максимальная длина строки — 256 символов")
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
        # переводимые названия модели в единственном и множественном числе.
        verbose_name = _("категория")
        verbose_name_plural = _("Категории")
        
    def __str__(self):
        return self.title


class Location(models.Model):
    """
    Модель локации для постов в блоге.
    """
    # название локации.
    name = models.CharField(
        max_length=256,
        verbose_name=_("Название места"),
        help_text=_("Максимальная длина строки — 256 символов")
    )
    # флаг видимости
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Опубликовано"),
        help_text=_("Снимите галочку, чтобы скрыть локацию")
    )
    # автоматически установленная дата создания
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Добавлено")
    )

    class Meta:
        # переводы названий модели в единственном и множественном числе.
        verbose_name = _("местоположение")
        verbose_name_plural = _("Местоположения")

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель поста в блоге."""
    # заголовок поста
    title = models.CharField(
        verbose_name=_("Заголовок"),
        max_length=256,
        help_text=_("Максимальная длина строки — 256 символов")
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
    # флаг публикации, по умолчанию True, можно скрыть пост.
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Опубликовано"),
        help_text=_("Снимите галочку, чтобы скрыть публикацию")
    )   
    # дата создания
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Добавлено")
    )
    
    class Meta:
        # переводимые названия модели в единственном и множественном числе.
        verbose_name = _("публикация")
        verbose_name_plural = _("Публикации")

    def __str__(self):
        return self.title

