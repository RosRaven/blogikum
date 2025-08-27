from django.contrib import admin

from .models import Category, Location, Post, Comment


# декоратор, регистрирует модель в админке.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #  поля, выводимые в списке записей.
    list_display = ("title", "is_published", "created_at")
    # автозаполнение slug из title
    prepopulated_fields = {"slug": ("title",)}

    # # В CategoryAdmin можно добавить list_filter = ("is_published",) 
    # # и search_fields = ("name",), чтобы было удобнее искать.
    # list_filter = ("is_published",)  # боковой фильтр по статусу
    # search_fields = ("name", "slug")  # поиск по имени и slug
    

# декоратор, регистрирует модель в админке.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    #  поля, выводимые в списке записей.
    list_display = ("name", "is_published", "created_at")

    # # Аналогично, как и в CategoryAdmin можно добавить фильтрацию и поиск.
    # list_filter = ("is_published",)  # боковой фильтр по статусу
    # search_fields = ("name",)  # поиск по имени


# декоратор, регистрирует модель в админке.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    #  поля, выводимые в списке записей.
    list_display = ("title", "author", "category", "location", "is_published", "pub_date")
    # боковой фильтр по статусу, категории и локации.
    list_filter = ("is_published", "category", "location")
    # добавляет в верх списка навигацию по дате pub_date.
    date_hierarchy = "pub_date"

    # # В PostAdmin можно расширить search_fields (("title", "text", "author__username")) 
    # search_fields = ("title", "text", "author__username")  # поиск по заголовку, тексту и имени автора


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "author", "created_at", )
    search_fields = ("text", )
    list_filter = ("created_at", )
    