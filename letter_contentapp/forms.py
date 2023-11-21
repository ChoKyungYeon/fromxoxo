from django import forms
from django.forms import ModelForm

from letter_contentapp.models import Letter_content


class Letter_contentCreateForm(ModelForm):

    class Meta:
        model = Letter_content
        fields = ('tema', 'content','image')
        labels = {
            'tema': ' ',
            'content': '',
            'image': '',
        }

        widgets = {
            'tema': forms.Select(attrs={'class': 'select field-tema', 'id': 'field-tema'}),
            'content': forms.Textarea(attrs={'placeholder': '내용을 작성해 주세요! 언제든 조정할 수 있습니다',
                                          'class': 'textarea', 'id': 'field-content'}),
            'image': forms.FileInput(attrs={ 'class': 'fileinput',}),
        }
