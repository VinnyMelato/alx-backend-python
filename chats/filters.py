# chats/filters.py
import django_filters
from chats.models import Message


class MessageFilter(django_filters.FilterSet):
    # Specific users: Filter by username (assumes sender/recipient are User FKs)
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='iexact')
    recipient = django_filters.CharFilter(field_name='recipient__username', lookup_expr='iexact')

    # Time range: Custom for created_at (e.g., ?created_after=2025-11-01&created_before=2025-11-23)
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        # List model fields that should be exposed; custom filters are declared above.
        fields = ['sender', 'recipient', 'created_at']