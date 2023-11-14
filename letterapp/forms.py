from django import forms
from django.core.validators import MaxLengthValidator

from letterapp.models import Letter


class LetterCreateForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ('state',)
        labels = {
        }
        widgets = {
            'state': forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].required = False



class LetterSearchForm(forms.Form):
    letter_url = forms.CharField(
        label=(""),
        widget=forms.TextInput(attrs={
            'placeholder': '복사한 링크를 입력해 주세요!',
            'class': 'textinput field-letter_url',
            'autofocus': True,
            'id':'field-letter_url'
        })
    )