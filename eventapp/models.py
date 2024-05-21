import uuid
from django.db import models

# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=2000, null=True)
    gift = models.TextField(max_length=2000, null=True)
    image = models.ImageField(upload_to='event/', null=True, blank=True)
    count = models.IntegerField(default=0)

    def can_read(self):
        return self.count > 2

    def count_left(self):
        return 3 - self.count