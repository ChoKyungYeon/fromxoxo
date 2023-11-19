import re
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, FormView, TemplateView
from django.utils.decorators import method_decorator

from fromxoxo.utils import is_user_related, quiz_session_key
from letter_quizapp.decorators import *
from letterapp.models import Letter
from letter_quizapp.forms import *
from letter_quizapp.models import Letter_quiz


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Letter_quizCreateDecorator, name='dispatch')
class Letter_quizCreateView(CreateView):
    model = Letter_quiz
    template_name = 'letter_quizapp/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.type = request.GET.get('type', None)
        self.target_letter = get_object_or_404(Letter, pk=self.kwargs['pk'])
        if not self.type or self.type not in ['choice','word','date']:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.type == 'choice':
            return Letter_quizChoiceCreateForm
        elif self.type == 'word':
            return Letter_quizWordCreateForm
        else:
            return Letter_quizDateCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_letter'] = self.target_letter
        context['tema'] = self.target_letter.letter_content.tema
        context['type'] = self.request.GET.get('type', None)
        context['page'] = 'create'
        return context

    def form_valid(self, form):
        valid_pattern = re.compile(r'^[a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣0-9\s]+$')
        with transaction.atomic():
            if self.type == 'word':
                wordanswer = form.cleaned_data['wordanswer']
                if not valid_pattern.match(wordanswer):
                    form.add_error('wordanswer', '한글, 영어, 숫자만 입력이 가능해요!')
                    return self.form_invalid(form)

            form.instance.letter = self.target_letter
            form.instance.type = self.type
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('letter_quizapp:list', kwargs={'pk': self.target_letter.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Letter_quizEditDecorator, name='dispatch')
class Letter_quizUpdateView(UpdateView):
    model = Letter_quiz
    template_name = 'letter_quizapp/update.html'
    context_object_name = 'target_quiz'

    def dispatch(self, request, *args, **kwargs):
        target_quiz=get_object_or_404(Letter_quiz, pk=self.kwargs['pk'])
        self.type = target_quiz.type
        self.target_letter = target_quiz.letter
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.type == 'choice':
            return Letter_quizChoiceCreateForm
        elif self.type == 'word':
            return Letter_quizWordCreateForm
        else:
            return Letter_quizDateCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_letter'] = self.target_letter
        context['tema'] = self.target_letter.letter_content.tema
        context['type'] = self.request.GET.get('type', None)
        context['page'] = 'update'
        return context

    def form_valid(self, form):
        valid_pattern = re.compile(r'^[a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣0-9\s]+$')
        with transaction.atomic():
            if self.type == 'word':
                wordanswer = form.cleaned_data['wordanswer']
                if not valid_pattern.match(wordanswer):
                    form.add_error('wordanswer', '한글, 영어, 숫자만 입력이 가능해요!')
                    return self.form_invalid(form)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('letter_quizapp:list', kwargs={'pk': self.target_letter.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Letter_quizListDecorator, name='dispatch')
class Letter_quizListView(DetailView):
    model = Letter
    template_name = 'letter_quizapp/list.html'
    context_object_name = 'target_letter'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quizs'] = self.object.letter_quiz.all().order_by('created_at')
        context['tema'] = self.object.letter_content.tema
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(Letter_quizEditDecorator, name='dispatch')
class Letter_quizDeleteView(DeleteView):
    model = Letter_quiz
    context_object_name = 'target_letter_quiz'
    template_name = 'letter_quizapp/delete.html'

    def get_success_url(self):
        return reverse_lazy('letter_quizapp:list', kwargs={'pk': self.object.letter.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(Letter_quizVerifyDecorator, name='dispatch')
class Letter_quizVerifyView(FormView):
    model = Letter_quiz
    template_name = 'letter_quizapp/verify.html'

    def dispatch(self, request, *args, **kwargs):
        self.target_quiz= get_object_or_404(Letter_quiz, pk=self.kwargs['pk'])
        self.type = self.target_quiz.type
        self.target_letter = self.target_quiz.letter
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.type == 'choice':
            return Letter_quizChoiceVerifyForm
        elif self.type == 'word':
            return Letter_quizWordVerifyForm
        else:
            return Letter_quizDateVerifyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_letter'] = self.target_letter
        context['target_quiz'] = self.target_quiz
        context['tema'] = self.target_letter.letter_content.tema
        return context

    def form_valid(self, form):
        with transaction.atomic():
            if self.type == 'word':
                user_answer = form.cleaned_data['wordanswer'].replace(" ", "").lower()
                quiz_answer = self.target_quiz.wordanswer.replace(" ", "").lower()
                if user_answer != quiz_answer:
                    if len(user_answer) != len(quiz_answer):
                        form.add_error('wordanswer', '정답의 단어 수가 달라요!')

                    else:
                        letter_difference = 0
                        for a, b in zip(user_answer, quiz_answer):
                            if a != b:
                                letter_difference += 1
                        form.add_error('wordanswer', f'{letter_difference}개의 단어가 일치하지 않아요!')
                    return self.form_invalid(form)

            elif self.type == 'choice':
                user_choice = set(form.cleaned_data['choiceanswer'])
                quiz_choice = set(self.target_quiz.choiceanswer)
                if user_choice != quiz_choice:
                    if len(user_choice) == 1 and len(quiz_choice) > 1:
                        form.add_error('choiceanswer', '모든 정답을 선택해 주세요!')

                    else:
                        form.add_error('choiceanswer', '정답이 정확하지 않습니다!')
                    return self.form_invalid(form)
            else:
                user_date = form.cleaned_data['dateanswer']
                quiz_date = self.target_quiz.date
                if user_date != quiz_date:
                    if user_date > quiz_date:
                       form.add_error('dateanswer', '더 과거의 날짜를 선택해 주세요!')

                    else:
                       form.add_error('dateanswer', '더 미래의 날짜를 선택해 주세요!')
                    return self.form_invalid(form)

            self.request.session[quiz_session_key(self.target_letter,self.target_quiz)] = True
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('letterapp:detail', kwargs={'pk': self.target_letter.pk})



@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Letter_quizPreviewDecorator, name='dispatch')
class Letter_quizPreviewView(TemplateView):
    model = Letter_quiz
    template_name = 'letter_quizapp/preview.html'


    def get_context_data(self, **kwargs):
        target_quiz = get_object_or_404(Letter_quiz, pk=self.kwargs['pk'])
        target_letter = self.object.letter
        context = super().get_context_data(**kwargs)
        context['target_letter'] = target_letter
        context['target_quiz'] = target_quiz
        context['tema'] = target_letter.letter_content.tema
        return context
