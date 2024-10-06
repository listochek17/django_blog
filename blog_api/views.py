from django.contrib.auth.models import User
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from blog_app.models import Category, Comment, Article
from .serializers import (CategorySerializer, CommentSerializer, ArticleSerializer, UserRegistrationSerializer,
                          UserLoginSerializer)
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView



# get, post
# get, put, delete
@extend_schema(tags=['Auth'])
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()


@extend_schema(tags=['Auth'])
class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(
            username=request.data['username'],
            password=request.data['password']
        )
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'invalid credentials'})


#

def api_root(request):
    endpoints = [
        'categories/',
        'categories/{pk}/',
        'comments/',
        'comments/{pk}/',
    ]
    return JsonResponse(endpoints, safe=False)


# api/categories/
# Category.objects.all() QuerySet
# values() - конвертирует в dict

# api/categories/
# api/categories/{id}/
# api/comments/
# api/comments/{id}

# def api_categories_list(request):
#     result = []
#     categories = Category.objects.all()
#     for category in categories:
#         result.append({
#             'id': category.pk,
#             'title': category.title,
#             'slug': category.slug
#         })
#
#     return HttpResponse(json.dumps(result, ensure_ascii=False),
#                         content_type='application/json')


# GET, POST, PUL, DELETE

# @api_view(['GET', 'POST'])
# def api_categories_list(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#     else:
#         serializer = CategorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()  # запускается метод create() внутри CategorySerializer
#         return Response(serializer.data)


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


"""
{
    "title": "new category",
    "slug": "new-category"
}
"""


# @api_view(['GET', 'PUT', 'DELETE'])  # PUT, DELETE
# def api_category_detail(request, pk):
#     category = Category.objects.get(pk=pk)
#
#     if request.method == 'GET':
#         serializer = CategorySerializer(category, many=False)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CategorySerializer(category, data=request.data)  # instance=category, validated_data=request.data
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         category.delete()
#         return Response('deleted')


# api_comments_list
# api_categories_list
# переписать на классы

# @api_view(['GET'])
# def api_comments_list(request):
#     comments = Comment.objects.all()
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# @api_view(['GET'])
# def api_comments_detail(request, pk):
#     comment = Comment.objects.get(pk=pk)
#     serializer = CommentSerializer(comment, many=False)
#     return Response(serializer.data)


class ArticleListView(generics.ListCreateAPIView):
    # get, post
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


# GET, POST,
# GET, PUT, DELETE, PATCH

@extend_schema(tags=['Categories'])
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=['Comments'])
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@extend_schema(tags=['Articles'])
class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('category', 'author')
    ordering_fields = ('views', 'created_at')
