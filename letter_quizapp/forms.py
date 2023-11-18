from django import forms
from django.forms import ModelForm
from letter_quizapp.models import Letter_quiz


class Letter_quizChoiceCreateForm(ModelForm):
    class Meta:
        model = Letter_quiz
        fields = ('question','image','choice1','choice2','choice3','choiceanswer')
        labels = {
            'question': '상대방에게 보이는 질문',
            'image': '',
            'choice1': '보기를 작성하고 답을 체크해요!',
            'choice2': '',
            'choice3': '',
            'choiceanswer':''
        }

        widgets = {
            'question': forms.Textarea(attrs={'placeholder': '둘만이 알고 있는 간결한 질문을 작성해요.','class': 'textarea'}),
            'image': forms.FileInput(attrs={'class': 'fileinput'}),
            'choice1': forms.TextInput(attrs={'placeholder': '1번 선택지', 'class': 'textinput field-choice'}),
            'choice2': forms.TextInput(attrs={'placeholder': '2번 선택지', 'class': 'textinput field-choice'}),
            'choice3': forms.TextInput(attrs={'placeholder': '3번 선택지', 'class': 'textinput field-choice'}),
            'choiceanswer': forms.CheckboxSelectMultiple(attrs={ 'class': 'selectmultiple','id': 'field-choiceanswer'}),
        }

class Letter_quizWordCreateForm(ModelForm):
    class Meta:
        model = Letter_quiz
        fields = ('question','image','wordanswer')
        labels = {
            'question': '상대방에게 보이는 질문',
            'image': '',
            'wordanswer': '단답형 정답',
        }

        widgets = {
            'question': forms.Textarea(attrs={'placeholder': '둘만이 알고 있는 간결한 질문을 작성해요.','class': 'textarea'}),
            'image': forms.FileInput(attrs={'class': 'fileinput'}),
            'wordanswer': forms.TextInput(attrs={'placeholder': '영어/한글/숫자 (대소문자 미구분)', 'class': 'textinput','id': 'field-wordanswer'}),
        }

class Letter_quizDateCreateForm(ModelForm):
    class Meta:
        model = Letter_quiz
        fields = ('question','image','dateanswer')
        labels = {
            'question': '상대방에게 보이는 질문',
            'image': '',
            'dateanswer': '날짜 정답',
        }

        widgets = {
            'question': forms.Textarea(attrs={'placeholder': '둘만이 알고 있는 간결한 질문을 작성해요.','class': 'textarea'}),
            'image': forms.FileInput(attrs={'class': 'fileinput'}),
            'dateanswer':forms.DateInput(attrs={'type': 'date', 'class': 'dateinput'}),
        }

class Letter_quizWordVerifyForm(forms.Form):
    wordanswer = forms.CharField(
        label="",
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': '영어/한글/숫자 (대소문자 미구분)', 'class': 'textinput','id': 'field-wordanswer'}),
    )

class Letter_quizDateVerifyForm(forms.Form):
    dateanswer = forms.DateField(
        label="",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'dateinput'}),
    )



class Letter_quizChoiceVerifyForm(forms.Form):
    QuizAnswerChoice = (
        ('보기1', '✓'),
        ('보기2', '✓'),
        ('보기3', '✓'),
    )
    choiceanswer = forms.MultipleChoiceField(
        choices=QuizAnswerChoice,
        label="",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'selectmultiple', 'id': 'field-choiceanswer'}),
    )