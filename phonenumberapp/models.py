import uuid
from datetime import timedelta, datetime
from django.db import models

from accountapp.models import CustomUser


class Phonenumber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=11)
    verification_code = models.CharField(max_length=6)
    is_verified=models.BooleanField(default=False)
    error_count=models.IntegerField(default=0)
    created_at =models.DateTimeField(auto_now_add=True)

    def timeout(self):
        elapsed_time = datetime.now() - self.created_at
        remaining_time = timedelta(minutes=3) - elapsed_time
        remaining_time_in_sec = max(remaining_time, timedelta(0)).total_seconds()
        return round(remaining_time_in_sec)