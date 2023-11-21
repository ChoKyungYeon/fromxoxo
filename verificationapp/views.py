import random
import uuid
from datetime import datetime, timedelta
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth import login
from accountapp.models import CustomUser
from fromxoxo.decorators import *
from verificationapp.decorators import *
from fromxoxo.sms import Send_SMS
from verificationapp.forms import *
from verificationapp.models import Verification
from django.contrib.auth import get_user_model


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_unrequired, name='dispatch')
@method_decorator(VerificationCreateDecorator, name='dispatch')
class VerificationCreateView(CreateView):
    model = Verification
    template_name = 'verificationapp/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.type = request.GET.get('type', None)
        return super().dispatch(request, *args, **kwargs)


    def get_form_class(self):
        return VerificationUpdateForm if self.type == 'update' else VerificationCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.type
        return context

    def form_valid(self, form):
        phonenumber = form.cleaned_data['phonenumber']
        type = self.type
        phonenumbers = get_user_model().objects.values_list('phonenumber', flat=True)
        with transaction.atomic():
            if len(phonenumber) < 11 or phonenumber[:3] != '010':
                form.add_error('phonenumber', '정확한 전화번호를 입력해 주세요')
                return self.form_invalid(form)

            if type == 'search' and phonenumber not in phonenumbers:
                form.add_error('phonenumber', '가입되지 않은 전화번호 입니다.')
                return self.form_invalid(form)

            if type != 'search' and phonenumber in phonenumbers:
                form.add_error('phonenumber', '이미 존재하는 전화번호입니다.')
                return self.form_invalid(form)

            form.instance.code = random.randint(100000, 999999)

            to = form.instance.phonenumber
            content = f'인증번호 {form.instance.code}를 3분 내에 입력해 주세요'
            Send_SMS(to, content, True)

            form.instance.type = self.type
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('verificationapp:verify', kwargs={'pk': self.object.pk})


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_unrequired, name='dispatch')
@method_decorator(VerificationVerifyDecorator, name='dispatch')
class VerificationVerifyView(FormView):
    model = Verification
    form_class = PhoneNumberVerifyForm
    template_name = 'verificationapp/verify.html'

    def dispatch(self, request, *args, **kwargs):
        self.target_verification = get_object_or_404(Verification, pk=self.kwargs['pk'])
        self.type = self.target_verification.type
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.type
        context['target_verification'] = self.target_verification
        context['remaining_time'] = self.target_verification.timeout()
        context['redirect_url'] = f"{reverse('verificationapp:create')}?type={self.type}"
        return context


    def form_valid(self, form):
        code = form.cleaned_data['code']
        error_count = self.target_verification.error_count
        with transaction.atomic():
            if len(code) < 6:
                form.add_error('code', '인증번호 6자리를 입력해 주세요')
                return self.form_invalid(form)
            
            if self.target_verification.code != code:
                if error_count == 4:
                    self.target_verification.delete()
                    return HttpResponseRedirect(f"{reverse('verificationapp:create')}?type={self.type}")

                else:
                    self.target_verification.error_count = error_count + 1
                    self.target_verification.save()
                    form.add_error('code', f'인증 코드 오류 횟수 ({self.target_verification.error_count}/5)')
                    return self.form_invalid(form)
            else:
                if self.type == 'signup':
                    self.target_verification.is_verified = True
                    self.target_verification.save()
                    self.request.session['object_pk'] = str(self.target_verification.pk)
                    return HttpResponseRedirect(reverse('accountapp:create', kwargs={'pk': self.kwargs['pk']}))
                
                elif self.type == 'update':
                    user = self.request.user
                    user.phonenumber = self.target_verification.phonenumber
                    user.save()
                    self.target_verification.delete()
                    return HttpResponseRedirect(reverse('accountapp:setting', kwargs={'pk': user.pk}))

                else:
                    user = CustomUser.objects.get(phonenumber=self.target_verification.phonenumber)
                    if user is not None:
                        login(self.request, user)
                    self.target_verification.delete()
                    return HttpResponseRedirect(reverse('accountapp:passwordreset', kwargs={'pk': self.request.user.pk}))
