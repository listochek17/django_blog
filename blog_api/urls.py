from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('comments', views.CommentViewSet)
router.register('articles', views.ArticleViewSet)


urlpatterns = [
    # functions
    # path('categories/', views.api_categories_list),
    # path('categories/<int:pk>/', views.api_category_detail),
    # path('comments/', views.api_comments_list),
    # path('comments/<int:pk>/', views.api_comments_detail),
    # path('', views.api_root),

    # Classes
    # path('categories/', views.CategoryList.as_view()),
    # path('categories/<int:pk>/', views.CategoryDetailView.as_view()),
    # path('comments/', views.CommentList.as_view()),
    # path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    # path('articles/', views.ArticleListView.as_view()),
    # path('articles/<int:pk>/', views.ArticleDetailView.as_view()),

    path('register/', views.UserRegistrationView.as_view()),
    path('login/', views.UserLoginView.as_view()),
]
# http://127.0.0.1:8000/api/


urlpatterns += router.urls

# drf-spectacular
