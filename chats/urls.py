from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, ChatViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'chats', ChatViewSet)
urlpatterns = [path('', include(router.urls))]