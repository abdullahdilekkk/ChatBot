from django.db import models

# Create your models here.
class ChatSession(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk
    

class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    #ChatSession dan Message objesine direkt erişmek için "messages" kullanılır

    sender = models.CharField(max_length=10)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"@{self.sender}-{self.created}\n{self.text}"