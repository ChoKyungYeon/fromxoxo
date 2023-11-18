import uuid

from django.db import models

from letterapp.models import Letter
from fromxoxo.utils import time_before


class Letter_info(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    letter = models.OneToOneField(Letter, on_delete=models.CASCADE, related_name='letter_info')
    sender = models.CharField(max_length=10, null=True)
    title = models.CharField(max_length=25, null=True)
    receiver = models.CharField(max_length=10, null=True)
    written_at = models.DateField(null=True)
