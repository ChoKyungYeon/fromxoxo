from django import forms
from django.forms import ModelForm
from letter_quizapp.models import Letter_quiz


class Letter_quizChoiceCreateForm(ModelForm):
    class Meta:
        model = Letter_quiz
        fields = ('question','image','choice1','choice2','choice3','choiceanswer')
        labels = {
            'question': '상대방이 해결할 질문',
            'image': '',
            'choice1': '보기를 작성하고 답을 체크해요!',
            'choice2': '',
            'choice3': '',
            'choiceanswer':''
        }

        widgets = {
            'question': forms.Textarea(attrs={'placeholder': '받는 사람과 보내는 사람만이 알 수 있는 질문 작성!','class': 'textarea field-question'}),
            'image': forms.FileInput(attrs={'class': 'fileinput field-image'}),
            'choice1': forms.TextInput(attrs={'placeholder': '1번 선택지', 'class': 'textinput field-choice'}),
            'choice2': forms.TextInput(attrs={'placeholder': '2번 선택지', 'class': 'textinput field-choice'}),
            'choice3': forms.TextInput(attrs={'placeholder': '3번 선택지', 'class': 'textinput field-choice'}),
            'choiceanswer': forms.CheckboxSelectMultiple(attrs={ 'class': 'selectmultiple' ,'id': 'field-choiceanswer'}),
        }

class Letter_quizAnswerCreateForm(ModelForm):
    class Meta:
        model = Letter_quiz
        fields = ('question','image','answer')
        labels = {
            'question': '상대방이 해결할 질문',
            'image': '',
            'answer': '질문 정답',
        }

        widgets = {
            'question': forms.Textarea(attrs={'placeholder': '받는 사람과 보내는 사람만이 알 수 있는 질문 작성!','class': 'textarea'}),
            'image': forms.FileInput(attrs={'class': 'fileinput'}),
            'answer': forms.TextInput(attrs={'placeholder': '영어 한글 숫자로 이루어진 답!', 'class': 'textinput','id': 'field-answer'}),
        }

class Letter_quizDateCreateForm(ModelForm):
    class Meta:
        model = Letter_quiz
        fields = ('question','image','date')
        labels = {
            'question': '상대방이 해결할 질문',
            'image': '',
            'date': '정답 날짜',
        }

        widgets = {
            'question': forms.Textarea(attrs={'placeholder': '받는 사람과 보내는 사람만이 알 수 있는 질문 작성!','class': 'textarea'}),
            'image': forms.FileInput(attrs={'class': 'fileinput'}),
            'date':forms.DateInput(attrs={'placeholder': '정답', 'type': 'date', 'class': 'dateinput'}),
        }

class Letter_quizAnswerVerifyForm(forms.Form):
    compare_answer = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': '영어 한글 숫자로 이루어진 답!', 'class': 'textinput','id': 'field-answer'}),
    )

class Letter_quizDateVerifyForm(forms.Form):
    compare_date = forms.DateField(
        label="",
        widget=forms.DateInput(attrs={'placeholder': '정답', 'type': 'date', 'class': 'dateinput'}),
    )



class Letter_quizChoiceVerifyForm(forms.Form):
    quizanswerchoice = (
        ('보기1', '✓'),
        ('보기2', '✓'),
        ('보기3', '✓'),
    )
    compare_choice = forms.MultipleChoiceField(
        choices=quizanswerchoice,
        label="",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'selectmultiple', 'id': 'field-choiceanswer'}),
    )