from django.contrib import admin
from .models import Conversation,Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
  list_display = ('id', 'created_at','updated_at')
  filter_horizontal = ('participants',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
  list_display = ('sender', 'conversation', 'content', 'timestamp', 'is_read' , 'is_deleted')
  list_filter = ('is_read' , 'is_deleted' , 'message_type')
  search_fields = ('content' , 'sender__username')  