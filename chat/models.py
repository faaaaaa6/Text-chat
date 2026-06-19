from django.db import models
from accounts.models import CustomUser

class Conversation(models.Model):
  participants = models.ManyToManyField(CustomUser, related_name='conversations')
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"conversation {self.id}"
  
class Message(models.Model):
     MESSAGE_TYPE=[
        ('text','Text'),
        ('image','Image'),
        ('file','File'),  
     ]  

     conversation = models.ForeignKey(Conversation,on_delete=models.CASCADE, related_name='message')
     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='sent_message')
     content = models.TextField(blank=True , null=True)
     message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE , default='text')
     attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)
     is_deleted = models.BooleanField(default=False)
     deleted_at = models.DateTimeField(null=True, blank=True)
     is_edited = models.BooleanField(default=False)
     edited_at = models.DateTimeField(null=True, blank=True)
     reply_to=models.ForeignKey('self',on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

     def __str__(self):
        return f"{self.sender.username}: {self.content[:50] if self.content else 'attachemnt'}"
     
     class Meta:
        ordering =['timestamp']


