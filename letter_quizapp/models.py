import uuid

from django.db import models
from multiselectfield import MultiSelectField
import re
from letterapp.models import Letter
from fromxoxo.choice import quiztypechoice, quizanswerchoice


# Create your models here.
class Letter_quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='letter_quiz')
    question = models.TextField(max_length=300)
    image = models.ImageField(upload_to='letter_quiz/', null=True, blank=True)
    type = models.CharField(max_length=20, choices=quiztypechoice)
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(max_length=51, null=True)
    choice1 = models.TextField(max_length=23, null=True)
    choice2  = models.TextField(max_length=23, null=True)
    choice3  = models.TextField(max_length=23, null=True)
    choiceanswer  = MultiSelectField(max_length=40, choices=quizanswerchoice, null=True)
    date = models.DateField(null=True)


    def index(self):
        return self.letter.letter_quiz.filter(created_at__lt=self.created_at).count()+1

    def next_url(self):
        return self.letter.letter_quiz.filter(created_at__lt=self.created_at).count()+1

    def answer_count(self):
        return len(self.answer.replace(" ", "")) if self.answer else 0

    def choiceanswer_hint(self):
        return ', '.join(self.choiceanswer)