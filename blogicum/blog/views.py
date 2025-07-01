from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# автоматически редиректит анонимов на страницу логина.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
# для отложенного вычисления success_url.
from django.urls import reverse_lazy
# готовая CBV для страниц создания объектов.
from django.views.generic import CreateView 

from .constants import POSTS_ON_MAIN
from .forms import PostForm
from .models import Post, Category


def _get_base_queryset():
    return Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
            ).order_by("-pub_date")


def index(request):
    post_list = _get_base_queryset()[:POSTS_ON_MAIN]
    return render(request, "blog/index.html", {"post_list": post_list})


from django.http import Http404


def post_detail(request, post_id):
    qs = Post.objects.filter(
        id=post_id,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    # если автор — даже если is_published=False, даём посмотреть
    if request.user.is_authenticated:
        qs = qs | Post.objects.filter(id=post_id, author=request.user)
    post = get_object_or_404(qs)
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects
            .filter(
                slug=category_slug, 
                is_published=True
                )
            )
    post_list = _get_base_queryset().filter(category=category)
    
    return render(
        request, 
        "blog/category.html", 
        {
            "category": category,
            "post_list": post_list
        }
    )


# LoginRequiredMixin — проверяет, что пользователь залогинен, 
# и если нет, автоматически перенаправляет на страницу логина.
# CreateView — готовый generic view, который сам разберёт GET/POST, валидацию формы и сохранение объекта.
# порядок миксинов имеет значение — LoginRequiredMixin должен стоять до CreateView.
class PostCreateView(LoginRequiredMixin, CreateView):
    #  указываем, какой модели соответствует эта view.
    model = Post
    # наша ModelForm
    form_class = PostForm
    # шаблон, где рендерится форма.
    template_name = "blog/post_form.html"
    # куда уезжаем после удачного сохранения.
    success_url = reverse_lazy("blog:index")

    # def get_success_url(self):
    #     # уезжать на страницу детали, вместо index,
    #     return reverse_lazy("blog:post_detail", kwargs={"post_id": self.object.pk})

    def form_valid(self, form):
        # вызывается, когда форма прошла валидацию
        # ещё не сохранённый объект Post.
        form.instance.author = self.request.user
        # Проставляем нужное поле и кидаем обратно в логику CreateView, где он сохранится и выполнится редирект.
        return super().form_valid(form)


# не даёт анонимным пользователям попасть на страницу создания.
@login_required
def post_create(request):
    # 1) При GET просто показываем пустую форму
    if request.method == "GET":
        form = PostForm()
        return render(request, 'blog/post_form.html', {"form": form})

    # 2) При POST обрабатываем отправленные данные
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # request.FILES для будущих полей файлов
        # запускает все проверки (clean_… и встроенные).
        if not form.is_valid():
            # Если форма не прошла валидацию, снова рендерим шаблон с ошибками
            return render(request, 'blog/post_form.html', {'form': form})

    # 3) Сохраняем объект, но ещё не в БД, чтобы проставить автора
    post = form.save(commit=False)
    post.author = request.user
    post.save()

    # 4) После успешного сохранения — редирект на детальный просмотр
    return redirect('blog:post_detail', post_id=post.pk)


class SignUpView(CreateView):
    # Это встроенный UserCreationForm с минимальным набором полей (username, password1, password2).
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


@login_required
def custom_logout(request):
    """
    Выходит из системы и сразу перенаправляет на главную страницу.
    Работает по GET и POST.
    """
    logout(request)
    return redirect('blog:index')
