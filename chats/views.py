from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # 👈 add this
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    renderer_classes = [JSONRenderer]  # 👈 force JSON only

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(users)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    renderer_classes = [JSONRenderer]  # 👈 force JSON only

    def perform_create(self, serializer):
        sender_id = self.request.data.get('sender')
        conversation_id = self.request.data.get('conversation')
        sender = User.objects.get(user_id=sender_id)
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        serializer.save(sender=sender, conversation=conversation)
