from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
]

