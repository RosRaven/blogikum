from django.db import models
from django.db.models import SET_NULL, CASCADE
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Category(models.Model):
    """
    Модель категории для постов в блоге.
    """
    title = models.CharField(
        max_length=256,
        unique=True,
        verbose_name=_("Название"),
        help_text=_("Максимальная длина строки — 256 символов")
    )
    description = models.TextField(
        verbose_name=_("Описание"),
        help_text=_("Краткое описание категории")
    )
    slug = models.SlugField(
        verbose_name=_("Идентификатор"),
        unique=True,
        help_text=_("Уникальный слаг для URL")
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Опубликовано"),
        help_text=_("Снимите галочку, чтобы скрыть категорию")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Добавлено")
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        

class Location(models.Model):
    """
    Модель локации для постов в блоге.
    """
    name = models.CharField(
        max_length=256,
        verbose_name=_("Название места"),
        help_text=_("Максимальная длина строки — 256 символов")
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Опубликовано"),
        help_text=_("Снимите галочку, чтобы скрыть локацию")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Добавлено")
    )

    class Meta:
        verbose_name = _("Местоположение")
        verbose_name_plural = _("Местоположения")


class Post(models.Model):
    """Модель поста в блоге."""
    title = models.CharField(
        max_length=256,
        verbose_name=_("Заголовок"),
        help_text=_("Максимальная длина строки — 256 символов")
    )
    text = models.TextField(verbose_name=_("Текст"))
    pub_date = models.DateTimeField(
        verbose_name=_("Дата публикации"),
        help_text=_("Если установить в будущем — отложенная публикация")
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name=_("Автор")
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=False,
        on_delete=CASCADE,
        verbose_name=_("Категория")
    )   
    location = models.ForeignKey(
        Location,
        on_delete=SET_NULL,
        verbose_name=_("Местоположение"),
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Добавлено")
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Опубликовано"),
        help_text=_("Снимите галочку, чтобы скрыть публикацию")
    )

    class Meta:
        verbose_name = _("Публикация")
        verbose_name_plural = _("Публикации")

    def __str__(self):
        return self.title

