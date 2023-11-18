from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django import forms
from django.core.validators import MaxLengthValidator
from accountapp.models import CustomUser


class AccountLoginForm(AuthenticationForm):
    username = UsernameField(
        label=(""),
        widget=forms.TextInput(attrs={
            'placeholder': '사용자 아이디',
            'class': 'textinput',
            'autofocus': True,
            'oninput': 'this.value = this.value.slice(0, 12);'
        }),
        validators=[MaxLengthValidator(12)],
        max_length=12
    )

    password = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '비밀번호',
            'class': 'textinput-nolabel',
            'autocomplete': 'current-password'
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                self.add_error('username', '')
                self.add_error('password', '잘못된 아이디 또는 비밀번호입니다.')
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class AccountCreateForm(UserCreationForm):
    password1 = forms.CharField(
        label=("비밀번호"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '영문/숫자/특수문자 혼합 8~20자',
            'class': 'textinput',
            'autocomplete': 'new-password',
        }),
    )

    password2 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "위와 동일한 비밀번호를 입력해 주세요",
            'class': 'textinput-nolabel',
            'autocomplete': 'new-password'
        }),
    )
    class Meta:
        model = CustomUser
        fields = ('username','password1', 'password2', 'agree_terms')
        labels = {
            'username': '사용자 아이디',
            'agree_terms': '전체 동의',
        }

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '6-12자의 영문/숫자/기호', 'class': 'textinput'}),
            'agree_terms': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }



class AccountUsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)
        labels = {
            'username': '사용자 아이디',
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '6-12자의 영문/숫자/기호', 'class': 'textinput'}),
        }

class AccountPasswordUpdateForm(UserCreationForm):
    password1 = forms.CharField(
        label=("새 비밀번호 "),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '영문/숫자/특수문자 혼합 8~20자',
            'class': 'textinput',
            'autocomplete': 'new-password',
        }),
    )

    password2 = forms.CharField(
        label=(""),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "동일한 비밀번호를 입력해 주세요",
            'class': 'textinput-nolabel',
            'autocomplete': 'new-password'
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')


class AccountPasswordResetForm(UserCreationForm):
    password1 = forms.CharField(
        label=("새 비밀번호 "),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': '영문/숫자/특수문자 혼합 8~20자',
            'class': 'textinput',
            'autocomplete': 'new-password',
        }),
    )

    password2 = forms.CharField(
        label=("비밀번호 확인"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "동일한 비밀번호를 입력해 주세요",
            'class': 'textinput',
            'autocomplete': 'new-password',
        }),
    )

    class Meta:
        model = CustomUser
        fields = ('username','password1', 'password2',)
        labels = {
            'username': '사용자 아이디',
        }

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '6-12자의 영문/숫자/기호', 'value': 'defaultUsername','class': 'textinput'}),
        }
