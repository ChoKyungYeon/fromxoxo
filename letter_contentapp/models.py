import uuid
from django.db import models

from fromxoxo.utils import time_before
from letterapp.models import Letter
from fromxoxo.choice import LetterThemeChoice


class Letter_content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    letter = models.OneToOneField(Letter, on_delete=models.CASCADE, related_name='letter_content')
    theme = models.CharField(max_length=20, choices=LetterThemeChoice, default='christmas')
    content = models.TextField(max_length=2000, null=True)
    image = models.ImageField(upload_to='letter_content/', null=True, blank=True)
    saved_at = models.DateTimeField(null=True)
