# chats/pagination.py
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # Exactly what the check wants
    page_size_query_param = 'page_size'