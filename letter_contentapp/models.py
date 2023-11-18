import uuid
from django.db import models
from letterapp.models import Letter
from fromxoxo.choice import LetterTemaChoice


class Letter_content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    letter = models.OneToOneField(Letter, on_delete=models.CASCADE, related_name='letter_content')
    tema = models.CharField(max_length=20, choices=LetterTemaChoice, default='pink')
    content = models.TextField(max_length=2000, null=True)
    image = models.ImageField(upload_to='letter_content/', null=True, blank=True)