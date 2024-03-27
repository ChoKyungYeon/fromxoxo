from vocaapp.models import Voca
from django import forms

class VocaCreateForm(forms.ModelForm):
    class Meta:
        model = Voca
        fields = ('word', 'meaning',)
        labels = {
            'word': '영어 단어',
            'meaning': '한국어',
        }
        widgets = {
            'word': forms.TextInput(attrs={'placeholder': '영어 단어를 입력해 주세요', 'class': 'textinput'}),
            'meaning': forms.TextInput(attrs={'placeholder': '한국어 의미를 입력해 주세요', 'class': 'textinput'}),
        }