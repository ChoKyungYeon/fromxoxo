from django import forms
from django.forms import ModelForm

from letter_infoapp.models import Letter_info


class Letter_infoCreateForm(ModelForm):
    class Meta:
        model = Letter_info
        fields = ('title','sender_name', 'receiver_name', 'written_at')
        labels = {
            'title': '제목',
            'sender_name': '작성자',
            'receiver_name': '수신자',
            'written_at': '날짜',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '간단한 편지 제목', 'class': 'textinput'}),
            'sender_name': forms.TextInput(attrs={'placeholder': '편지에 표시되는 작성자 별명!', 'class': 'textinput'}),
            'receiver_name': forms.TextInput(attrs={'placeholder': '편지에 표시되는 수신자 별명!', 'class': 'textinput'}),
            'written_at': forms.DateInput(attrs={'placeholder': '작성일', 'type': 'date', 'class': 'dateinput'}),
        }
