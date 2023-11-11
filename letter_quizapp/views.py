import re
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, TemplateView, RedirectView, FormView
from accountapp.models import CustomUser
from django.utils.decorators import method_decorator

from letter_quizapp.forms import *
from letterapp.models import Letter
from letter_quizapp.forms import *
from letter_quizapp.models import Letter_quiz


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class Letter_quizCreateView(CreateView):
    model = Letter_quiz
    template_name = 'letter_quizapp/create.html'
    def get_form_class(self):
        type_param = self.request.GET.get('type', None)
        if type_param == 'choice':
            return Letter_quizChoiceCreateForm
        elif type_param == 'answer':
            return Letter_quizAnswerCreateForm
        else:
            return Letter_quizDateCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_letter = get_object_or_404(Letter, pk=self.kwargs['pk'])
        context['target_letter'] = target_letter
        context['type'] = self.request.GET.get('type', None)
        return context

    def form_valid(self, form):
        target_letter = get_object_or_404(Letter, pk=self.kwargs['pk'])
        type_param = self.request.GET.get('type', None)
        valid_pattern = re.compile(r'^[a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣0-9\s]+$')
        with transaction.atomic():
            form.instance.letter = target_letter
            form.instance.type = type_param
            form.instance.save()
            if type_param == 'answer':
                answer = form.cleaned_data['answer']
                if not valid_pattern.match(answer):
                    form.add_error('answer', '한글, 영어, 숫자만 입력이 가능해요!')
                    return self.form_invalid(form)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('letter_quizapp:list', kwargs={'pk': self.kwargs['pk']})


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class Letter_quizUpdateView(UpdateView):
    model = Letter_quiz
    template_name = 'letter_quizapp/update.html'
    context_object_name = 'target_quiz'

    def get_form_class(self):
        type_param = self.object.type
        if type_param == 'choice':
            return Letter_quizChoiceCreateForm
        elif type_param == 'answer':
            return Letter_quizAnswerCreateForm
        else:
            return Letter_quizDateCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_letter'] = self.object.letter
        context['type'] = self.object.type
        return context

    def form_valid(self, form):
        type_param = self.object.type
        valid_pattern = re.compile(r'^[a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣0-9\s]+$')
        with transaction.atomic():
            if type_param == 'answer':
                answer = form.cleaned_data['answer']
                if not valid_pattern.match(answer):
                    form.add_error('answer', '한글, 영어, 숫자만 입력이 가능해요!')
                    return self.form_invalid(form)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('letter_quizapp:list', kwargs={'pk': self.object.letter.pk})




@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class Letter_quizDetailView(DetailView):
    model = Letter_quiz
    template_name = 'letter_quizapp/detail.html'
    context_object_name = 'target_letter_quiz'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_letter'] = self.object.letter
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class Letter_quizListView(DetailView):
    model = Letter
    template_name = 'letter_quizapp/list.html'
    context_object_name = 'target_letter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_letter = get_object_or_404(Letter, pk=self.kwargs['pk'])
        context['quizs'] = target_letter.letter_quiz.all().order_by('created_at')
        context['progress'] = 3
        return context


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class Letter_quizGuideView(DetailView):
    model = Letter
    template_name = 'letter_quizapp/guide.html'
    context_object_name = 'target_letter'





class Letter_quizExpireView(TemplateView):
    template_name = 'letter_quizapp/expire.html'



@method_decorator(login_required, name='dispatch')
class Letter_quizDeleteView(DeleteView):
    model = Letter_quiz
    context_object_name = 'target_letter_quiz'
    template_name = 'letter_quizapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('letter_quizapp:list', kwargs={'pk': self.object.letter.pk})


class Letter_quizVerifyView(FormView):
    model = Letter_quiz
    template_name = 'letter_quizapp/verify.html'

    def get_form_class(self):
        type_param = get_object_or_404(Letter_quiz, pk=self.kwargs['pk']).type
        if type_param == 'choice':
            return Letter_quizChoiceVerifyForm
        elif type_param == 'answer':
            return Letter_quizAnswerVerifyForm
        else:
            return Letter_quizDateVerifyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        letter_quiz= get_object_or_404(Letter_quiz, pk=self.kwargs['pk'])
        context['target_letter'] = letter_quiz.letter
        context['target_quiz'] = letter_quiz
        context['quizstep'] = letter_quiz.index()
        context['type'] = letter_quiz.type
        context['quiz_len'] = letter_quiz.letter.letter_quiz.all().count()
        return context

    def form_valid(self, form):
        letter_quiz= get_object_or_404(Letter_quiz, pk=self.kwargs['pk'])
        target_letter= letter_quiz.letter
        type_param = letter_quiz.type
        target_user=self.request.user
        session_key = f"quizstep_{self.kwargs['pk']}"
        with transaction.atomic():
            if type_param == 'answer':
                compare_answer = form.cleaned_data['compare_answer'].replace(" ", "").lower()
                quiz_answer = letter_quiz.answer.replace(" ", "").lower()
                if compare_answer != quiz_answer:
                    if len(compare_answer) != len(quiz_answer):
                        form.add_error('compare_answer', '정답의 단어 수가 달라요!')
                    else:
                        letter_difference = 0
                        for a, b in zip(compare_answer, quiz_answer):
                            if a != b:
                                letter_difference += 1
                        form.add_error('compare_answer', f'{letter_difference}개의 단어가 일치하지 않아요!')
                    return self.form_invalid(form)

            elif type_param == 'choice':
                compare_choice = set(form.cleaned_data['compare_choice'])
                quiz_choice = set(letter_quiz.choiceanswer)
                if compare_choice != quiz_choice:
                    if len(compare_choice) == 1 and len(quiz_choice) > 1:
                        form.add_error('compare_choice', '모든 정답을 선택해 주세요!')
                    else:    
                        form.add_error('compare_choice', '정답이 정확하지 않습니다!')
                    return self.form_invalid(form)
            else:
                compare_date = form.cleaned_data['compare_date']
                quiz_date = letter_quiz.date
                if compare_date != quiz_date:
                    if compare_date > quiz_date:
                       form.add_error('compare_date', '더 과거의 날짜를 선택해 주세요!')
                    else:
                       form.add_error('compare_date', '더 미래의 날짜를 선택해 주세요!')
                    return self.form_invalid(form)

            self.next_quiz = letter_quiz.letter.letter_quiz.all().order_by('created_at').filter(
                created_at__gt=letter_quiz.created_at).first()
            if self.next_quiz:
                self.request.session[session_key] = letter_quiz.index()+1
            else:
                is_user_related = target_user in [target_letter.receiver, target_letter.sender]
                if not is_user_related:
                    target_letter.state = 'checked'
                    target_letter.checked_at = datetime.now()
                    target_letter.save()
                self.request.session[session_key] = 'done'
            return super().form_valid(form)

    def get_success_url(self):
        letter_quiz = get_object_or_404(Letter_quiz, pk=self.kwargs['pk'])
        return reverse_lazy('letter_quizapp:verify', kwargs={'pk': self.next_quiz.pk})\
            if self.next_quiz else reverse_lazy('letterapp:detail', kwargs={'pk': letter_quiz.letter.pk})
