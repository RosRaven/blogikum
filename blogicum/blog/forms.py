from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'location', 'category', 'image')
        widjets = {
            # Удобный ввод даты/времени (работает в современных браузерах)
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
