import datetime

from django.db import models, transaction
from accountapp.models import CustomUser
from fromxoxo.choice import progresschoice
import random
import string
from io import BytesIO
from django.core.files.base import ContentFile
from django.urls import reverse
import qrcode
from fromxoxo.utils import time_before
import secrets
import string
import uuid

# Create your models here.
class Letter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='letter_sender', null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='letter_receiver', null=True)
    is_checked = models.BooleanField(default=False)
    is_received = models.BooleanField(default=False)
    checked_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    progress = models.CharField(max_length=20, choices=progresschoice, default='progress1')
    qr = models.ImageField(upload_to='letter/')
    url = models.CharField(max_length=100)

    def finished_before(self):
        return time_before(self.finished_at)

    def character_number(self):
        return random.randint(1, 23)

    def generate_url(self):
        base_url = reverse('letterapp:intro', kwargs={'pk': self.pk})
        return f'http://13.209.69.42{base_url}'

    def generate_qrcode(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((512, 512))
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()



