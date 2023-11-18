import uuid
from datetime import timedelta, datetime
from django.db import models
from fromxoxo.choice import VerificationTypeChoice


class Verification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phonenumber = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    is_verified=models.BooleanField(default=False)
    error_count=models.IntegerField(default=0)
    created_at =models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=VerificationTypeChoice)

    def timeout(self):
        elapsed_time = datetime.now() - self.created_at
        remaining_time = timedelta(minutes=3) - elapsed_time
        remaining_time_in_sec = max(remaining_time, timedelta(0)).total_seconds()
        return round(remaining_time_in_sec)