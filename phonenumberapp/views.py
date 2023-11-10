import random
import uuid
from urllib.parse import urlencode
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, FormView
from django.contrib.auth import login
from accountapp.models import CustomUser
from letterapp.models import Letter
from phonenumberapp.decorators import *
from fromxoxo.sms import Send_SMS
from phonenumberapp.forms import PhonenumberCreateForm, PhoneNumberVerifyForm, PhonenumberUpdateForm
from phonenumberapp.models import Phonenumber
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator


@method_decorator(PhonenumberCreateDecorator, name='dispatch')
class PhonenumberCreateView(CreateView):
    model = Phonenumber
    form_class = PhonenumberCreateForm
    template_name = 'phonenumberapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.request.GET.get('type', None)
        return context

    def form_valid(self, form):
        number = form.cleaned_data['number']
        type_param = self.request.GET.get('type', None)
        phonenumbers = get_user_model().objects.values_list('phonenumber', flat=True)
        with transaction.atomic():
            if len(number) <11 or number[:3] != '010':
                form.add_error('number', '정확한 전화번호를 입력해 주세요')
                return self.form_invalid(form)
            if type_param == 'search':
                if number not in phonenumbers:
                    form.add_error('number', '가입되지 않은 전화번호 입니다.')
                    return self.form_invalid(form)
            else:
                if number in phonenumbers:
                    form.add_error('number', '이미 존재하는 전화번호입니다.')
                    return self.form_invalid(form)

            try:  # deploy check
                import fromxoxo.settings.local
                form.instance.verification_code=111111
            except:
                form.instance.verification_code=random.randint(100000, 999999)
            form.instance.save()
            to = form.instance.number
            content = f'인증번호 {form.instance.verification_code}를 3분 내에 입력해 주세요'
            Send_SMS(to, content, True)
            return super().form_valid(form)


    def get_success_url(self):
        type_param = self.request.GET.get('type', None)
        if type_param == 'signup':
            base_url = reverse_lazy('phonenumberapp:verify', kwargs={'pk': self.object.pk})
        elif type_param == 'update':
            base_url = reverse_lazy('phonenumberapp:verify', kwargs={'pk': self.object.pk})
        else:
            base_url = reverse_lazy('phonenumberapp:verify', kwargs={'pk': self.object.pk})
        if type_param:
            query_string = urlencode({'type': type_param})
            return f'{base_url}?{query_string}'
        return base_url




@method_decorator(PhonenumberVerifyDecorator, name='dispatch')
class PhonenumberVerifyView(FormView):
    model = Phonenumber
    form_class = PhoneNumberVerifyForm
    template_name = 'phonenumberapp/verify.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_param = self.request.GET.get('type', None)
        phonenumber= get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        context['type'] = type_param
        context['phonenumber'] = phonenumber
        context['remaining_time'] = phonenumber.timeout()
        base_url = reverse('phonenumberapp:create')
        if type_param == 'signup':
            context['redirect_url']=f"{base_url}?type=signup"
        elif type_param == 'search':
            context['redirect_url']=f"{base_url}?type=search"
        else:
            context['redirect_url']=f"{base_url}?type=update"

        return context

    def form_valid(self, form):
        type_param=self.request.GET.get('type', None)
        compare_code = form.cleaned_data['compare_code']
        phonenumber= get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        error_count = phonenumber.error_count
        with transaction.atomic():
            if len(compare_code) < 6:
                form.add_error('compare_code', '인증번호 6자리를 입력해 주세요')
                return self.form_invalid(form)
            if phonenumber.verification_code == compare_code:
                if type_param == 'signup':
                    phonenumber.is_verified = True
                    phonenumber.save()
                    self.request.session['verification_code'] = phonenumber.verification_code
                    return HttpResponseRedirect(reverse_lazy('accountapp:create', kwargs={'pk': self.kwargs['pk']}))
                elif type_param == 'update':
                    target_user = self.request.user
                    target_user.phonenumber = phonenumber.number
                    target_user.save()
                    phonenumber.delete()
                    return HttpResponseRedirect(reverse_lazy('accountapp:setting', kwargs={'pk': self.request.user.pk}))
                else:
                    user = CustomUser.objects.get(phonenumber=phonenumber.number)
                    if user is not None:
                        login(self.request, user)
                    phonenumber.delete()
                    letter_pk = self.request.session.get("letter_pk", False)
                    if letter_pk:
                        letter_uuid = uuid.UUID(letter_pk)
                        if Letter.objects.filter(pk=letter_uuid).first():
                            self.request.session["redirection_letter"] = None
                            return redirect('letterapp:detail', pk=letter_uuid)
                    return HttpResponseRedirect(reverse_lazy('accountapp:reset', kwargs={'pk': self.request.user.pk}))
            else:
                if error_count == 4:
                    phonenumber.delete()
                    base_url = reverse('phonenumberapp:create')
                    if type_param == 'signup':
                        return HttpResponseRedirect(f"{base_url}?type=signup")
                    elif type_param == 'search':
                        return HttpResponseRedirect(f"{base_url}?type=search")
                    else:
                        return HttpResponseRedirect(f"{base_url}?type=update")
                else:
                    phonenumber.error_count = error_count + 1
                    phonenumber.save()
                    form.add_error('compare_code', f'인증 코드 오류 횟수 ({phonenumber.error_count}/5)')
                    return self.form_invalid(form)





