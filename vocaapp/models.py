import uuid
from django.db import models

from accountapp.models import CustomUser


class Voca(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='voca')
    meaning = models.CharField(max_length=30)
    word = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)

