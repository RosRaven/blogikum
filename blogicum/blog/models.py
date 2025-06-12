from django.db import models
from django.urls import reverse


class Category(models.Model):
    # обычное текстовое поле.
    name = models.CharField(    
        max_length=100,
        unique=True, # гарантирует на уровне БД, что дубликатов не будет.
        help_text="Название категории, должно быть уникальным" # опционально, помогает в админке и документации.
    )
    # то же, но с валидацией «слуга» (только латиница/цифры/дефис/подчёркивание).
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="ЧПУ для URL, на основе name"
    )

    # новое поле: необязательное текстовое описание
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Краткое описание для пользователей",
        blank=True,     # можно не заполнять
        null=False,     # в БД будет пустая строка, а не NULL
    )

    # строковое представление объекта, полезно в админке и отладке.
    def __str__(self):
        return self.name
    
    # даёт прямую ссылку на страницу объекта.
    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField() # TextField для больших текстов.
    created_at = models.DateTimeField(auto_now_add=True) # auto_now_add=True автоматически проставляет дату создания.
    # ForeignKey создаёт «многие-к-одному» связь.
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE, # CASCADE удаляет посты, если категория удалена.
        related_name="posts" # related_name позволяет обращаться к постам через категорию.
        # Например, category.posts.all() вернёт все посты в этой категории.
    )
    published_at = models.DateTimeField(
        verbose_name="Дата публикации",
        null=True,      # может быть NULL в БД
        blank=True,     # не обязательно заполнять в форме
    )

    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ("archived", "В архиве"),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="Статус публикации",
        help_text="Черновик — не виден на основном сайте"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})
    
    class Meta:
        # добавим сортировку: сначала «черновики», потом «опубликованные», затем «архив»
        ordering = ["status", "-created_at"]

    
