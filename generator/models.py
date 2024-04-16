from django.db import models
import uuid


class Token(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ReceivedData(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=1)  # Neue Versionierung

    def __str__(self):
        return f"{self.key} v{self.version}: {self.value} (Token: {self.token})"
