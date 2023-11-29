from django import forms
from django.forms import ModelForm

from letter_contentapp.models import Letter_content


class Letter_contentCreateForm(ModelForm):

    class Meta:
        model = Letter_content
        fields = ('theme', 'content','image')
        labels = {
            'theme': ' ',
            'content': '',
            'image': '',
        }

        widgets = {
            'theme': forms.Select(attrs={'class': 'select field-theme', 'id': 'field-theme'}),
            'content': forms.Textarea(attrs={'placeholder': '내용을 작성해 주세요! 언제든 조정할 수 있습니다',
                                          'class': 'textarea', 'id': 'field-content'}),
            'image': forms.FileInput(attrs={ 'class': 'fileinput',}),
        }
