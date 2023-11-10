import uuid
from datetime import timedelta, datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from fromxoxo.choice import userstatechoice

username_validator = UnicodeUsernameValidator()

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=13, unique=True,validators=[username_validator],error_messages={
            'unique': "이미 존재하는 아이디입니다.",
        })
    phonenumber = models.CharField(max_length=11, unique=True)
    can_receive_notification = models.BooleanField(default=True)
    agree_terms = models.BooleanField(blank=True, null=True)
    state = models.CharField(max_length=20, choices=userstatechoice, default='normal')

