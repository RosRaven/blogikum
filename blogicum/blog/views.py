from django.shortcuts import render

# 0) Список «постов», из которого мы берём данные
posts = [{
         'id': 0,         
         'location': 'Остров отчаянья',
         'date': '30 сентября 1659 года',         
         'category': 'travel',
         'text': '''
         Наш корабль, застигнутый в открытом море
         страшным штормом, потерпел крушение.
         Весь экипаж, кроме меня, утонул; я же,
         несчастный Робинзон Крузо, был выброшен
         полумёртвым на берег этого проклятого острова,
         который назвал островом Отчаяния.''',
     },     {
         'id': 1,         
         'location': 'Остров отчаянья',
         'date': '1 октября 1659 года',         
         'category': 'not-my-day',
         'text': '''
         Проснувшись поутру, я увидел, что наш корабль сняло
         с мели приливом и пригнало гораздо ближе к берегу.
         Это подало мне надежду, что, когда ветер стихнет,
         мне удастся добраться до корабля и запастись едой и
         другими необходимыми вещами. Я немного приободрился,
         хотя печаль о погибших товарищах не покидала меня.
         Мне всё думалось, что, останься мы на корабле, мы
         непременно спаслись бы. Теперь из его обломков мы могли бы
         построить баркас, на котором и выбрались бы из этого
         гиблого места.''',
     },     {
         'id': 2,         
         'location': 'Остров отчаянья',
         'date': '25 октября 1659 года',         
         'category': 'not-my-day',
         'text': '''
         Всю ночь и весь день шёл дождь и дул сильный
         порывистый ветер. 25 октября.  Корабль за ночь разбило
         в щепки; на том месте, где он стоял, торчат какие-то
         жалкие обломки,  да и те видны только во время отлива.
         Весь этот день я хлопотал  около вещей: укрывал и
         укутывал их, чтобы не испортились от дождя.''',
     }, ]

def index(request):
    """
    1) Главная страница: отдаём все посты.
    render(request, template, context) 
    — оборачивает шаблон blog/index.html в HttpResponse,
      передавая ему context = {'posts': posts}.
    """
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, id):
    """
    2) Детальный просмотр одного поста:
    Параметр `id` приходит из URL (конвертер <int:id>).
    next(...) находит первый словарь в posts с таким id,
    либо None, если не найден.
    """
    # ищем словарь с нужным id
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        # если не нашли, возвращаем 404
        return render(request, '404.html', status=404)    
    
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """
    Показывает страницу «Публикации в категории X».
    Пока без списка самих постов, только название категории из URL.
    """
    return render(request, 'blog/category.html', {'category_slug': category_slug, })


# def category_posts(request, category_slug):
    # """
    # 3) Публикации по категории:
    # Параметр `category_slug` — строка из URL (<slug:category_slug>).
    # Фильтруем все p['category'] == category_slug
    # и отдаём шаблону blog/category.html два ключа:
    #   - 'category_slug' (для заголовка)
    #   - 'posts' — список отфильтрованных постов.
    # """
    # filtered = [post for post in posts if post['category'] == category_slug]
    # return render(request, 'blog/category.html', {'category_slug': category_slug, 'posts': filtered})