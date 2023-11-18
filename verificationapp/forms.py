from django import forms
from django.core.validators import MaxLengthValidator
from django.forms import ModelForm

from verificationapp.models import Verification


class VerificationCreateForm(ModelForm):
    class Meta:
        model = Verification
        fields = ('phonenumber',)
        labels = {
            'phonenumber': '전화번호'
        }

        widgets = {
            'phonenumber': forms.NumberInput(attrs={'placeholder': '- 제외 전화번호 11자',
                                                    'class': 'textinput',
                                                    'oninput': 'this.value = this.value.slice(0, 11);'}),
        }


class VerificationUpdateForm(ModelForm):
    class Meta:
        model = Verification
        fields = ('phonenumber',)
        labels = {
            'phonenumber': '새로운 전화번호'
        }
        widgets = {
            'phonenumber': forms.NumberInput(attrs={'placeholder': '- 제외 전화번호 11자',
                                                    'class': 'textinput',
                                                    'oninput': 'this.value = this.value.slice(0, 11);'}),
        }


class PhoneNumberVerifyForm(forms.Form):
    code = forms.CharField(
        label="인증 코드",
        widget=forms.NumberInput(attrs={'placeholder': '인증 코드 6자리 입력', 'class': 'textinput',
                                        'oninput': 'this.value = this.value.slice(0, 6);'}),
    )
