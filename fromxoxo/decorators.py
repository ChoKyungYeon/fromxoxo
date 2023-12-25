from datetime import datetime, timedelta

from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse

from accountapp.models import CustomUser
from letterapp.models import Letter
from verificationapp.models import Verification


def quiz_session_key(letter,quiz):
    return f'Letter:{letter.pk}Quiz:{quiz.pk}'

def login_unrequired(func):
    def decorated(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated


class Decorators:
    def __init__(self,request, **kwargs):
        self.request = request
        self.user = request.user
        self.letter = None
        if 'pk' in kwargs:
            self.object_pk = kwargs['pk']
        elif 'object_pk' in request.GET:
            self.object_pk = request.GET.get('object_pk')
        else:
            self.object_pk = None

    def register_session(self, session_key):
        session_value = self.request.GET.get(session_key, None)
        if session_value:
            self.request.session[session_key] = session_value

    def ownership_required(self):
        if self.user != get_object_or_404(CustomUser, pk=self.object_pk):
            return HttpResponseForbidden()

    def verification_required(self):
        if self.request.session.get("object_pk", None) != str(self.object_pk):
            return HttpResponseForbidden()

    def update_user(self):
        letters=list(self.user.letter_writer.filter(progress='done').all()) + list(self.user.letter_saver.all())
        for letter in letters:
            if letter.should_delete():
                letter.delete()  
                    
    def update_error(self):
        if self.letter and self.letter.should_reset_error():
            self.letter.errored_at = None
            self.letter.error = 0
            self.letter.save()

    def update_verification(self):
        for verification in Verification.objects.filter(is_verified=False):
            if datetime.now() - verification.created_at > timedelta(minutes=3):
                verification.delete()

    def check_verification(self):
        verification = get_object_or_404(Verification, pk=self.object_pk)
        if verification.is_verified:
            return HttpResponseForbidden()

    def get_letter(self, model, redirect):
        try:
            intance =get_object_or_404(model, pk=self.object_pk)
            self.letter = intance if isinstance(intance, Letter) else intance.letter
            
            if self.letter.should_delete():
                self.letter.delete()
                return HttpResponseRedirect(reverse('letterapp:expire') + '?type=none')

            if self.letter.is_user_related(self.user):
                if redirect:
                    return HttpResponseRedirect(reverse('letterapp:result', kwargs={'pk': self.letter.pk}))

            elif self.letter.state == 'saved':
                return HttpResponseRedirect(reverse('letterapp:expire') + '?type=saved')

        except Http404:
            return HttpResponseRedirect(reverse('letterapp:expire') + '?type=none')



    def role_required(self, role):
        if self.letter:
            role_checks = {
                'writer': self.letter.writer != self.user,
                'saver': self.letter.saver != self.user,
                'related': not self.letter.is_user_related(self.user),
                'unrelated': self.letter.is_user_related(self.user),
            }
            if role_checks[role]:
                return HttpResponseForbidden()

    def session_required(self,session_list):
        session_value = self.request.GET.get('type', None)
        if not session_value or session_value not in session_list:
            return HttpResponseForbidden()

    def state_required(self, state_list):
        if self.letter and self.letter.state not in state_list:
            return HttpResponseForbidden()

    def progress_required(self, progress_list):
        if self.letter and self.letter.progress not in progress_list:
            return HttpResponseForbidden()

    def can_add_quiz(self,):
        if self.letter and self.letter.quiz_len() >= 5:
            return HttpResponseForbidden()

    def is_locked(self):
        if self.letter and self.letter.is_locked():
            return HttpResponseForbidden()

    def quiz_redirector(self):
        if self.letter:
            letter_quizs=self.letter.letter_quiz.all().order_by('created_at')
            for letter_quiz in letter_quizs:
                if not self.request.session.get(quiz_session_key(self.letter,letter_quiz), None):
                    return HttpResponseRedirect(reverse('letter_quizapp:verify', kwargs={'pk': letter_quiz.pk}))

            if self.letter.state == 'unchecked':
                self.letter.state = 'checked'
                self.letter.expire_from = datetime.now()
                self.letter.save()
