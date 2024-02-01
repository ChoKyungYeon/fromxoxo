
import uuid
from django.db import models
from django.db.models.functions import TruncDate

from accountapp.models import CustomUser


# Create your models here.
class Analytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(unique=True)
    letter_count = models.IntegerField(default=0)

    def user_count(self):
        user_count = CustomUser.objects.annotate(
            created_date=TruncDate('created_at')
        ).filter(created_date=self.created_at).count()
        return user_count