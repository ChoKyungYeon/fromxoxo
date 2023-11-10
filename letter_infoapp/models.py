import uuid

from django.db import models

from letterapp.models import Letter
from fromxoxo.utils import time_before


class Letter_info(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    letter = models.OneToOneField(Letter, on_delete=models.CASCADE, related_name='letter_info')
    sender_name = models.CharField(max_length=8,null=True)
    title = models.CharField(max_length=30,null=True)
    receiver_name = models.CharField(max_length=8,null=True)
    written_at = models.DateField(null=True)
