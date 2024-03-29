import random
import uuid
from datetime import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from fromxoxo.choice import AccountCharaterChoice

username_validator = UnicodeUsernameValidator()


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=15, unique=True, validators=[username_validator],error_messages={
            'unique': "이미 존재하는 아이디입니다.",
        })
    phonenumber = models.CharField(max_length=11, unique=True)
    agree_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    character = models.CharField(max_length=20, choices=AccountCharaterChoice, default='character3')

    def __str__(self):
        return f"[{self.username}] {self.phonenumber}"

