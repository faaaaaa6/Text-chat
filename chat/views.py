from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Conversation , Message
from . serializers import ConversationSerializer,MessageSerializer
from accounts.models import CustomUser

class ConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        conversations = Conversation.objects.filter(participants=request.user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        conversation_id = request.data.get('conversation_id')
        content = request.data.get('content')

        try:   
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=status.HTTP_400_NOT_FOUND)
        
        message = Message.objects.create(
            conversation=conversation,
            sender = request.user,
            content=content
        )

        serializer = MessageSerializer(message)
        return Response ( serializer.data,status=status.HTTP_201_CREATED)

class CreateConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        user_id = request.data.get('user_id')

        try:
            other_user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND) 

        conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()

        if conversation:
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
       
    
            