from django.db import models
import uuid


class Token(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ReceivedData(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    data = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Data received at {self.received_at} with token {self.token}"
