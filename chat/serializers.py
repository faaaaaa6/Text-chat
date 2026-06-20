from rest_framework import serializers
from .models import Conversation, Message
from accounts.serializers import ProfileSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)

    class Meta:
        model = Message

        fields = ['id', 'conversation', 'sender', 'content', 'message_type', 
                   'attachment', 'timestamp', 'is_read', 'is_deleted', 'is_edited', 'reply_to']
        
        read_only_fields = ['sender', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    participants = ProfileSerializer(many=True, read_only=True) 
    last_message = serializers.SerializerMethodField()       

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at', 'last_message']

    def get_last_message(self,obj):
        last_msg = obj.message.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None    



