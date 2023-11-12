import uuid

from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, RedirectView
import re
from accountapp.forms import *
from accountapp.models import CustomUser
from letterapp.models import Letter
from phonenumberapp.models import Phonenumber
from django.utils.decorators import method_decorator

class AccountLoginView(LoginView):
    form_class = AccountLoginForm
    template_name = 'accountapp/login.html'
    success_url = reverse_lazy('homescreenapp:homescreen')


    def get(self, request, *args, **kwargs):
        redirect_letter = self.request.GET.get('redirect_letter', None)
        if redirect_letter:
            self.request.session['redirect_letter'] = redirect_letter
            print('1',self.request.session['redirect_letter'])
        if request.user.is_authenticated:
            return redirect('homescreenapp:homescreen')
        return super().get(request, *args, **kwargs)

@method_decorator(never_cache, name='dispatch')
class AccountCreateView(CreateView):
    model = CustomUser
    form_class = AccountCreateForm
    template_name = 'accountapp/create.html'
    success_url = reverse_lazy('accountapp:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_phonenumber'] = get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        phonenumber = get_object_or_404(Phonenumber, pk=self.kwargs['pk'])
        agree_terms = form.cleaned_data['agree_terms']
        usernames = get_user_model().objects.values_list('username', flat=True)
        username = form.cleaned_data['username']
        pattern = r'^[a-zA-Z0-9!@#$%^&*()_+{}|:"<>?`~\[\]\\;\',./-]+$'
        with transaction.atomic():
            if username in usernames:
                form.add_error('username','이미 존재하는 아이디입니다.')
                return self.form_invalid(form)

            if not 6 <= len(username) <= 12 or not re.match(pattern, username):
                form.add_error('username', '6-12자의 영문, 숫자, 기호를 입력해 주세요 ')
                return self.form_invalid(form)

            if not agree_terms == True:
                form.add_error('agree_terms', '약관 및 방침에 동의해 주세요')
                return self.form_invalid(form)

            form.instance.phonenumber = phonenumber.number
            form.instance.save()
            phonenumber.delete()
            return super().form_valid(form)

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AccountUsernameUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountUsernameUpdateForm
    template_name = 'accountapp/usernameupdate.html'

    def form_valid(self, form):
        usernames = get_user_model().objects.values_list('username', flat=True)
        username = form.cleaned_data['username']
        pattern = r'^[a-zA-Z0-9!@#$%^&*()_+{}|:"<>?`~\[\]\\;\',./-]+$'
        with transaction.atomic():
            if username == self.object.username:
                form.add_error('username','기존과 다른 아이디를 설정해 주세요.')
                return self.form_invalid(form)

            if username in usernames:
                form.add_error('username','이미 존재하는 아이디입니다.')
                return self.form_invalid(form)

            if not 6 <= len(username) <= 12 or not re.match(pattern, username):
                form.add_error('username', '6-12자의 영문, 숫자, 기호를 입력해 주세요 ')
                return self.form_invalid(form)
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accountapp:setting', kwargs={'pk': self.object.pk})


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AccountResetView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountResetForm
    template_name = 'accountapp/reset.html'
    success_url = reverse_lazy('accountapp:logout')

    def form_valid(self, form):
        usernames = get_user_model().objects.values_list('username', flat=True)
        username = form.cleaned_data['username']
        pattern = r'^[a-zA-Z0-9!@#$%^&*()_+{}|:"<>?`~\[\]\\;\',./-]+$'
        with transaction.atomic():
            if username in usernames and username != self.object.username:
                form.add_error('username','이미 존재하는 아이디입니다.')
                return self.form_invalid(form)

            if not 6 <= len(username) <= 12 or not re.match(pattern, username):
                form.add_error('username', '6-12자의 영문, 숫자, 기호를 입력해 주세요 ')
                return self.form_invalid(form)

            form.instance.save()
            return super().form_valid(form)

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AccountPasswordUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountPasswordUpdateForm
    success_url = reverse_lazy('accountapp:logout')
    template_name = 'accountapp/passwordupdate.html'


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AccountDeleteView(DeleteView):
    model = CustomUser
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'


@method_decorator(login_required, name='dispatch')
class AccountSettingView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'accountapp/setting.html'


@method_decorator(login_required, name='dispatch')
class AccountNotificationUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accountapp:setting', kwargs={'pk': self.request.GET.get('user_pk')})

    def get(self, request, *args, **kwargs):
        target_user = CustomUser.objects.get(pk=self.request.GET.get('user_pk'))
        target_user.can_receive_notification = True if target_user.can_receive_notification == False else False
        target_user.save()
        return super(AccountNotificationUpdateView, self).get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class AccountSentMailboxView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'accountapp/sentmailbox.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        letters=self.object.letter_sender.filter(progress='done').order_by('-finished_at')
        context['letters'] = letters
        context['letters_liked'] = letters.filter(letter_like__customuser=self.object)
        return context

@method_decorator(login_required, name='dispatch')
class AccountSavedMailboxView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'accountapp/savedmailbox.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        letters=self.object.letter_receiver.filter(progress='done').order_by('-finished_at')
        context['letters'] = letters
        context['letters_liked'] = letters.filter(letter_like__customuser=self.object)
        return context

