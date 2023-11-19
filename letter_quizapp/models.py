import uuid

from django.db import models
from multiselectfield import MultiSelectField
import re
from letterapp.models import Letter
from fromxoxo.choice import QuizTypeChoice, QuizAnswerChoice


# Create your models here.
class Letter_quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='letter_quiz')
    question = models.TextField(max_length=300)
    image = models.ImageField(upload_to='letter_quiz/', null=True, blank=True)
    type = models.CharField(max_length=20, choices=QuizTypeChoice)
    created_at = models.DateTimeField(auto_now_add=True)

    choice1 = models.TextField(max_length=25, null=True)
    choice2 = models.TextField(max_length=25, null=True)
    choice3 = models.TextField(max_length=25, null=True)

    choiceanswer = MultiSelectField(max_length=50, choices=QuizAnswerChoice, null=True)
    wordanswer = models.TextField(max_length=15, null=True)
    dateanswer = models.DateField(null=True)


    def letter_quizs(self):
        return self.letter.letter_quiz.all()

    def index(self):
        return self.letter_quizs().filter(created_at__lt=self.created_at).count()+1

    def next_quiz(self):
        return self.letter_quizs().order_by('created_at').filter(created_at__gt=self.created_at).first()

    def answer_count(self):
        return len(self.wordanswer.replace(" ", "")) if self.wordanswer else 0

