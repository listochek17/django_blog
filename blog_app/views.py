from django.shortcuts import render, HttpResponse, get_object_or_404, redirect

from django.views.generic import UpdateView, DeleteView
from .models import Category, Article, Comment, ArticleViews, SearchHistory, Like, Dislike
from .forms import LoginForm, RegisterForm, CommentForm, ArticleForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.auth.models import User

# Paginator
# from django.template.defaultfilters import slugify
# Create your views here.

# request - данные о странице где мы находимся

# [[1, [1,2,3,4]],[2, [5,6,7,8]],[3, [9,10]]]
# http://127.0.0.1:8000/?page=2
def home_view(request):
    # categories = Category.objects.all()
    articles = Article.objects.all()
    paginator = Paginator(articles, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    # query params
    history = []
    result = []
    if request.user.is_authenticated:
        history = set(request.user.search_history.all())
        for i in history:
            if i.text not in result:
                result.append(i.text)
    context = {
        # 'categories': categories
        'articles': articles,
        'history': result
    }
    return render(request, 'blog_app/index.html', context)


def contact_view(request):
    return render(request, 'blog_app/contacts.html')


def all_categories_page(request):
    articles = Article.objects.all()
    print(request.GET)

    query = request.GET.get('sort', '')
    if query:
        articles = articles.order_by(query)

    paginator = Paginator(articles, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'articles': articles,
        'category_title': 'Все категории'
    }
    return render(request, 'blog_app/categories.html', context)


def category_view(request, slug):
    category = Category.objects.get(slug=slug)
    # 1
    articles = Article.objects.filter(category=category)
    query = request.GET.get('sort', '')
    if query:
        articles = articles.order_by(query)

    paginator = Paginator(articles, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {
        'category': category,
        'category_title': category.title,
        'articles': articles
    }
    return render(request, 'blog_app/categories.html', context)


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = Comment.objects.filter(article=article)

    try:
        article.likes
    except Exception as e:
        print(e, e.__class__)
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        print(e, e.__class__)
        Dislike.objects.create(article=article)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            return redirect('detail', pk=pk)
    else:
        form = CommentForm()
    if not request.session.session_key:
        request.session.save()  # создаем ключ сессии

    session_key = request.session.session_key
    obj = ArticleViews.objects.filter(session_id=session_key, article=article)

    if obj.count() == 0 and session_key != 'None':
        new_obj = ArticleViews(article=article, session_id=session_key)
        new_obj.save()

        article.views += 1
        article.save()

    total_likes = article.likes.user.all().count()
    total_dislikes = article.dislikes.user.all().count()
    print(total_likes, total_dislikes)
    context = {
        'article': article,
        'form': form,
        'comments': comments,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes
    }
    return render(request, 'blog_app/detail.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'blog_app/login.html', context)


def registration_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'blog_app/registration.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')


def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('detail', pk=form.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, 'blog_app/article_form.html', context)


class UpdateArticle(UpdateView):
    model = Article
    form_class = ArticleForm
    success_url = '/'
    template_name = 'blog_app/article_form.html'


def profile_view(request, username):
    user_obj = User.objects.get(username=username)
    qs = Article.objects.filter(author=user_obj)
    paginator = Paginator(qs, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    total_comments = sum([article.comments.all().count() for article in qs])
    context = {
        'articles': articles,
        'user_obj': user_obj,
        'total_articles': qs.count(),
        'total_comments': total_comments
    }
    return render(request, 'blog_app/profile.html', context)


# Article, article_confirm_delete.html

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'blog_app/article_confirm_delete.html'
    success_url = '/'


def search(request):
    query = request.GET.get('q')
    history = []
    if request.user.is_authenticated:
        obj = SearchHistory(text=query, user=request.user)
        obj.save()
        history = set(request.user.search_history.all())

    articles = Article.objects.filter(title__iregex=query)
    context = {
        'articles': articles,
        'history': history
    }
    return render(request, 'blog_app/index.html', context)


def add_vote(request, article_id, action):
    # action='add_like'
    # action='add_dislike'
    article = get_object_or_404(Article, pk=article_id)

    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    if action == 'add_like':
        if request.user in article.likes.user.all():
            article.likes.user.remove(request.user.pk)
        else:
            article.likes.user.add(request.user.pk)
            article.dislikes.user.remove(request.user.pk)
    elif action == 'add_dislike':
        if request.user in article.dislikes.user.all():
            article.dislikes.user.remove(request.user.pk)
        else:
            article.dislikes.user.add(request.user.pk)
            article.likes.user.remove(request.user.pk)
    return redirect('detail', pk=article.pk)

