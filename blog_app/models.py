from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

# CREATE TABLE blog_app_category(
#  title VARCHAR()
# )

# Category object (1)
class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(null=True, verbose_name='Слаг')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'  # название модели в единственном числе
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    preview = models.ImageField(upload_to='images/articles/previews/', blank=True, null=True, verbose_name='Превью')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='articles')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Автор', related_name='articles',
                               null=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор',
                               related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья',
                                related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.article.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class ArticleViews(models.Model):
    session_id = models.CharField(max_length=150)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class SearchHistory(models.Model):
    text = models.CharField(max_length=500, verbose_name='Запрос поиска')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='search_history', verbose_name='Юзер')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Запрос поиска'
        verbose_name_plural = 'Запросы поиска'


class Like(models.Model):
    user = models.ManyToManyField(User, related_name='likes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE,
                                related_name='likes')


class Dislike(models.Model):
    user = models.ManyToManyField(User, related_name='dislikes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE,
                                related_name='dislikes')

class Todo(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Полное описание')
    created_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='todos')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

"""
таблица Comment
author - ссылка на таблицу User
article - ссылка на таблицу Article
text - текст комментария
created_at - дата и время создания комментария

сделать строковое представление класса

"""