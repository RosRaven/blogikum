from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Категории блога:
    - name: название (CharField, unique)
    - slug: ЧПУ для URL (SlugField)
    - description: необязательное описание
    """
    name = models.CharField(    
        max_length=100,
        unique=True, 
        help_text="Название категории, должно быть уникальным" 
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="ЧПУ для URL, на основе name"
    )

    
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Краткое описание для пользователей",
        blank=True,     
        null=False,     
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


class Post(models.Model):
    """
    Публикации блога: контент, категории и статусы.
    - title, slug — заголовок и ЧПУ
    - content — контент
    - category — связь с Category
    - status — состояние (черновик, опубликован, архив)
    - created_at, published_at — даты
    """
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True)
    content     = models.TextField() 
    location    = models.CharField(
        max_length=200,
        verbose_name="Местоположение",
        help_text="Где происходит действие публикации",
    )

    created_at  = models.DateTimeField(auto_now_add=True) 
    # 1) Сырой текст даты — отображение «как есть»
    event_date_raw = models.CharField(
        max_length=100,
        verbose_name="Дата события (сырой текст)",
        help_text="Дата в формате '1 октября 1659 года'",
    )
    # 2) Парсенная дата — для фильтрации, сортировки и т. д.
    event_date = models.DateField(
        verbose_name="Дата события",
        help_text="Автоматически создаётся из сырого текста, если возможно",
        null=True,
        blank=True, 
    )
    published_at = models.DateTimeField(
        verbose_name="Дата публикации", 
        null=True, 
        blank=True,
    )

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликован'
        ARCHIVED = 'archived', 'В архиве'
    
    # Связь с Category:
    # ForeignKey создаёт связь многие-к-одному:
    # CASCADE удаляет посты, если категория удалена.
    # related_name позволяет обращаться к постам через категорию.
    # Например, category.posts.all() вернёт все посты в этой категории.
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE, 
        related_name="posts" 
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Статус публикации",
        help_text="Черновик — не виден на основном сайте"
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})
    
    # добавим сортировку: сначала «черновики», потом «опубликованные», затем «архив»
    class Meta:
        ordering = ["status", "-created_at"]
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["-created_at"], name="post_created_desc"),
        ]
    
