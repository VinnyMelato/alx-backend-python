# chats/views.py
from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination  # Fallback
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Chat  # Adjust if needed
from .serializers import MessageSerializer, ChatSerializer  # Assuming these exist
from .filters import MessageFilter
from .pagination import MessagePagination
from .permissions import IsOwnerOrReadOnly  # From your earlier fix

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')  # Order for paginated lists
    serializer_class = MessageSerializer
    pagination_class = MessagePagination  # 20/page
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    pagination_class = MessagePagination  # Reuse for chats if needed
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter  # Or ChatFilter if separate
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]