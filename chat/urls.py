from django.urls import path
from .views import ConversationView , SendMessageView , CreateConversationView

urlpatterns = [
    path('conversation/',ConversationView.as_view(), name='conversation'),
    path('message/send/',SendMessageView.as_view(), name='send-message'),
    path('conversations/create/', CreateConversationView.as_view(), name='create-conversation')
]
