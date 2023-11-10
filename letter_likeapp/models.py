import uuid

from django.db import models

from accountapp.models import CustomUser
from letterapp.models import Letter


# Create your models here.


class Letter_like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='letter_like')
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='letter_like')

    class Meta:
        unique_together =('customuser', 'letter')