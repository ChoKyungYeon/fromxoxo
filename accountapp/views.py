import random

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, RedirectView
import re
from accountapp.decorators import *
from accountapp.forms import *
from fromxoxo.decorators import *
from verificationapp.models import Verification
from django.utils.decorators import method_decorator


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_unrequired, name='dispatch')
@method_decorator(AccountLoginDecorator, name='dispatch')
class AccountLoginView(LoginView):
    form_class = AccountLoginForm
    template_name = 'accountapp/login.html'
    success_url = reverse_lazy('homescreenapp:intro')



@method_decorator(never_cache, name='dispatch')
@method_decorator(login_unrequired, name='dispatch')
@method_decorator(AccountCreateDecorator, name='dispatch')
class AccountCreateView(CreateView):
    model = CustomUser
    form_class = AccountCreateForm
    template_name = 'accountapp/create.html'
    success_url = reverse_lazy('accountapp:login')

    def dispatch(self, request, *args, **kwargs):
        self.target_verification = get_object_or_404(Verification, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_verification'] = self.target_verification
        return context

    def form_valid(self, form):
        agree_terms = form.cleaned_data['agree_terms']
        username = form.cleaned_data['username']
        usernames = get_user_model().objects.values_list('username', flat=True)
        pattern = r'^[a-zA-Z0-9!@#$%^&*()_+{}|:"<>?`~\[\]\\;\',./-]+$'
        with transaction.atomic():
            if username in usernames:
                form.add_error('username', '이미 존재하는 아이디입니다.')
                return self.form_invalid(form)

            if not 6 <= len(username) <= 12 or not re.match(pattern, username):
                form.add_error('username', '6-12자의 영문, 숫자, 기호를 입력해 주세요 ')
                return self.form_invalid(form)

            if not agree_terms:
                form.add_error('agree_terms', '약관 및 방침에 동의해 주세요')
                return self.form_invalid(form)

            form.instance.phonenumber = self.target_verification.phonenumber
            form.instance.save()
            self.target_verification.delete()
            return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(AccountOwnershipDecorator, name='dispatch')
class AccountUsernameUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountUsernameUpdateForm
    template_name = 'accountapp/usernameupdate.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        usernames = get_user_model().objects.values_list('username', flat=True)
        pattern = r'^[a-zA-Z0-9!@#$%^&*()_+{}|:"<>?`~\[\]\\;\',./-]+$'
        with transaction.atomic():
            if username == self.object.username:
                form.add_error('username', '기존과 다른 아이디를 설정해 주세요.')
                return self.form_invalid(form)

            if username in usernames:
                form.add_error('username', '이미 존재하는 아이디입니다.')
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
@method_decorator(AccountOwnershipDecorator, name='dispatch')
class AccountPasswordResetView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'accountapp/passwordreset.html'
    form_class = AccountPasswordResetForm
    success_url = reverse_lazy('accountapp:logout')

    def form_valid(self, form):
        usernames = get_user_model().objects.values_list('username', flat=True)
        username = form.cleaned_data['username']
        pattern = r'^[a-zA-Z0-9!@#$%^&*()_+{}|:"<>?`~\[\]\\;\',./-]+$'
        with transaction.atomic():
            if username in usernames and username != self.object.username:
                form.add_error('username', '이미 존재하는 아이디입니다.')
                return self.form_invalid(form)

            if not 6 <= len(username) <= 12 or not re.match(pattern, username):
                form.add_error('username', '6-12자의 영문, 숫자, 기호를 입력해 주세요 ')
                return self.form_invalid(form)

            form.instance.save()
            return super().form_valid(form)

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(AccountOwnershipDecorator, name='dispatch')
class AccountPasswordUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountPasswordUpdateForm
    success_url = reverse_lazy('accountapp:logout')
    template_name = 'accountapp/passwordupdate.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(AccountOwnershipDecorator, name='dispatch')
class AccountDeleteView(DeleteView):
    model = CustomUser
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(AccountOwnershipDecorator, name='dispatch')
class AccountSettingView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'accountapp/setting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icon_int'] = random.randint(1, 20)
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(AccountOwnershipDecorator, name='dispatch')
class AccountNotificationUpdateView(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        self.target_user = CustomUser.objects.get(pk=self.request.GET.get('object_pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('accountapp:setting', kwargs={'pk': self.target_user.pk})

    def get(self, request, *args, **kwargs):
        self.target_user.can_receive_notification = True if self.target_user.can_receive_notification == False else False
        self.target_user.save()
        return super(AccountNotificationUpdateView, self).get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
@method_decorator(AccountCharacterUpdateDecorator, name='dispatch')
class AccountCharacterUpdateView(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        self.target_user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        self.type = self.request.GET.get('type', None)
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('accountapp:setting', kwargs={'pk': self.target_user.pk})

    def get(self, request, *args, **kwargs):
        self.target_user.character = self.type
        self.target_user.save()
        return super(AccountCharacterUpdateView, self).get(request, *args, **kwargs)


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(AccountLetterListDecorator, name='dispatch')
class AccountWriteListView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'accountapp/writelist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        letters = self.object.letter_writer.filter(progress='done').order_by('-finished_at')
        context['letters'] = letters
        context['letters_liked'] = letters.filter(letter_like__user=self.object)
        return context


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(AccountLetterListDecorator, name='dispatch')
class AccountSaveListView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'accountapp/savelist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        letters = self.object.letter_saver.filter(progress='done').order_by('-finished_at')
        context['letters'] = letters
        context['letters_liked'] = letters.filter(letter_like__user=self.object)
        return context
