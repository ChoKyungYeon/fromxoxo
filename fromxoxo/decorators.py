from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from fromxoxo.utils import is_user_related, quiz_session_key
from letter_contentapp.models import Letter_content
from letter_infoapp.models import Letter_info
from letter_likeapp.models import Letter_like
from letter_quizapp.models import Letter_quiz
from letterapp.models import Letter


def login_unrequired(func):
    def decorated(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated


class Decorators:
    def __init__(self, user, object_pk):
        self.user = user
        self.object_pk = object_pk
        self.letter = None

    def user_update(self):
        for letter in list(self.user.letter_writer.filter(progress='done').all()) + list(self.user.letter_saver.all()):
            if letter.should_delete():
                letter.delete()

    def user_owenership_required(self):
        if self.user.pk != self.object_pk:
            return HttpResponseForbidden()

    def instance_update(self, object_param):
        class_mapping = {
            'letter': Letter,
            'letter_content': Letter_content,
            'letter_info': Letter_info,
            'letter_quiz': Letter_quiz,
            'letter_like': Letter_like,
        }
        try:
            if object_param == 'letter':
                self.letter = get_object_or_404(Letter, pk=self.object_pk)
            else:
                instance_class = class_mapping.get(object_param)
                if instance_class:
                    instance = get_object_or_404(instance_class, pk=self.object_pk)
                    self.letter = instance.letter


            if self.letter.should_delete():
                self.letter.delete()
                return HttpResponseRedirect(reverse('letterapp:expire') + '?type=none')

            if self.letter.state == 'saved' and not is_user_related(self.user, self.letter):
                return HttpResponseRedirect(reverse('letterapp:expire') + '?type=saved')

        except Http404:
            return HttpResponseRedirect(reverse('letterapp:expire') + '?type=none')



    def instance_owenership_required(self, role):
        if self.letter:
            if role == 'writer':
                if self.letter.writer != self.user:
                    return HttpResponseForbidden()
            elif role == 'saver':
                if self.letter.saver != self.user:
                    return HttpResponseForbidden()
            elif role == 'related':
                if not is_user_related(self.user, self.letter):
                    return HttpResponseForbidden()
            elif role == 'unrelated':
                if is_user_related(self.user, self.letter):
                    return HttpResponseForbidden()

    def state_required(self, state_list):
        if self.letter and self.letter.state not in state_list:
            return HttpResponseForbidden()

    def can_add_quiz(self,):
        if self.letter and self.letter.quiz_len() >= 5:
            return HttpResponseForbidden()


    def progress_required(self, progress_list):
        if self.letter and self.letter.progress not in progress_list:
            return HttpResponseForbidden()


    def letter_redirector(self, object_param):
        try:
            if object_param == 'letter':
                self.letter = get_object_or_404(Letter, pk=self.object_pk)
            elif object_param == 'letter_quiz':
                instance = get_object_or_404(Letter_quiz, pk=self.object_pk)
                self.letter = instance.letter

            if self.letter.should_delete():
                self.letter.delete()
                return HttpResponseRedirect(reverse('letterapp:expire') + '?type=none')
            if self.letter.writer == self.user:
                return HttpResponseRedirect(reverse('letterapp:result', kwargs={'pk': self.letter.pk}))
            elif self.letter.saver == self.user:
                return HttpResponseRedirect(reverse('letterapp:result', kwargs={'pk': self.letter.pk}))
            else:
                if self.letter.state == 'saved':
                    return HttpResponseRedirect(reverse('letterapp:expire') + '?type=saved')

        except Http404:
            return HttpResponseRedirect(reverse('letterapp:expire') + '?type=none')


    def quiz_redirector(self,request):
        for letter_quiz in self.letter.letter_quiz.all().order_by('created_at'):
            if request.session.get(quiz_session_key(self.letter,letter_quiz), None):
                pass
            else:
                return HttpResponseRedirect(reverse('letter_quizapp:verify', kwargs={'pk': letter_quiz.pk}))