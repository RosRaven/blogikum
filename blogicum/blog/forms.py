from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # поля, которые будем редактировать через форму
        fields = [
            'title',
            'text',
            'pub_date',
            'location',
            'category',
            'is_published',
        ]
        widgets = {
            # HTML5-виджет для даты/времени
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'title': _('Заголовок'),
            'text': _('Текст'),
            'pub_date': _('Дата и время публикации'),
            'location': _('Местоположение'),
            'category': _('Категория'),
            'is_published': _('Опубликовано'),
        }
        help_texts = {
            'title': _('Максимум 256 символов'),
            'pub_date': _('Можно указать дату в будущем для отложенной публикации'),
        }

    def clean_title(self):
        # Методы валидации
        title = self.cleaned_data['title']
        if 'spam' in title.lower():
            raise forms.ValidationError(_('В заголовке нельзя использовать слово “spam”'))
        return title


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description', 'slug', 'is_published']
        labels = {
            'title': _('Заголовок категории'),
            'description': _('Описание'),
            'slug': _('Идентификатор для URL'),
            'is_published': _('Опубликовано'),
        }
        help_texts = {
            'slug': _('Латиница, цифры, дефис и подчёркивание'),
        }
