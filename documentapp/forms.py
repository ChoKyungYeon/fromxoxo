from django import forms

from documentapp.models import Document


class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document

        fields = ( 'termofuse', 'privacypolicy','announcement','blog','instagram', 'kakaotalk','phonenumber')

        labels = {
            'termofuse': '이용 약관 (노션 url)',
            'privacypolicy': '개인정보처리방침 (노션 url)',
            'announcement': '공지사항 (노션url)',
            'blog': '네이버 블로그 (url)',
            'kakaotalk': '오픈 카카오톡 (url)',
            'instagram': '인스타그램 (url)',
            'phonenumber': '고객센터 연락처',
        }

        widgets = {
            'termofuse': forms.Textarea(attrs={'class': 'textarea'}),
            'privacypolicy': forms.Textarea(attrs={'class': 'textarea'}),
            'announcement': forms.Textarea(attrs={'class': 'textarea'}),
            'blog': forms.Textarea(attrs={'class': 'textarea'}),
            'kakaotalk': forms.Textarea(attrs={'class': 'textarea'}),
            'instagram': forms.Textarea(attrs={'class': 'textarea'}),
            'phonenumber' : forms.TextInput(attrs={'class': 'textinput'}),
        }