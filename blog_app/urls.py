from django.urls import path
from . import views

# http://127.0.0.1:8000/
urlpatterns = [
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('categories/', views.all_categories_page, name='all_categories'),
    path('categories/<slug:slug>/', views.category_view, name='category'),
    path('articles/add/', views.create_article_view, name='create'),
    path('articles/<int:pk>/', views.article_detail, name='detail'),
    path('articles/<int:pk>/edit/', views.UpdateArticle.as_view(), name='edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='delete'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('authors/<str:username>/', views.profile_view, name='profile'),
    path('search/', views.search, name='search'),
    path('articles/<int:article_id>/<str:action>/', views.add_vote, name='add_vote')
]

# github copilot
# tabnine
# authors/<username>/
