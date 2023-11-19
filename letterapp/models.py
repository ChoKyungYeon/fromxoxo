from datetime import timedelta, datetime
from django.db import models
from accountapp.models import CustomUser
from fromxoxo.choice import LetterProgressChoice, LetterStateChoice
import random
from io import BytesIO
from django.urls import reverse
import qrcode
from fromxoxo.utils import time_before, time_after
import uuid
import pyshorteners
type_tiny = pyshorteners.Shortener()

class Letter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    writer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='letter_writer', null=True)
    saver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='letter_saver', null=True)

    expire_from = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    is_unsaved = models.BooleanField(default=False)
    progress = models.CharField(max_length=20, choices=LetterProgressChoice, default='progress1')
    state = models.CharField(max_length=20, choices=LetterStateChoice, default='unchecked')
    qr = models.ImageField(upload_to='letter/')
    url = models.CharField(max_length=100)

    def initial_quiz(self):
        return self.letter_quiz.all().order_by('created_at').first()

    def quiz_len(self):
        return self.letter_quiz.all().count()

    def finished_before(self):
        return time_before(self.finished_at)


    def delete_after(self):
        return time_after(self.expire_from, timedelta(hours=24)) if self.state == 'checked' else None


    def should_delete(self):#deploycheck
        return (datetime.now() - self.expire_from) > timedelta(hours=24) if self.state == 'checked' else None

    def character_number(self):
        return random.randint(1, 23)

    def generate_url(self):
        base_url = reverse('letterapp:intro', kwargs={'pk': self.pk})
        full_url = f'https://www.fromxoxo.com{base_url}'
        return type_tiny.tinyurl.short(full_url)


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

    def state_text(self):
        if self.state == 'unchecked':
            return '미확인'
        elif self.state == 'checked':
            return '저장 해제' if self.is_unsaved else '확인 완료'
        else:
            return '저장 완료'