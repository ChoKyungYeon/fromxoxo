from datetime import datetime
import re
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, DeleteView, UpdateView, TemplateView, CreateView, RedirectView, FormView
from accountapp.models import CustomUser
from django.utils.decorators import method_decorator

from letter_contentapp.models import Letter_content
from letter_infoapp.models import Letter_info
from letter_likeapp.models import Letter_like
from letterapp.forms import *
from letterapp.models import Letter




@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class LetterResultView(DetailView):
    model = Letter
    template_name = 'letterapp/result.html'
    context_object_name = 'target_letter'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.request.GET.get('page', None)
        return context

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class LetterFinishView(DetailView):
    model = Letter
    template_name = 'letterapp/finish.html'
    context_object_name = 'target_letter'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class LetterSavedView(DetailView):
    model = Letter
    template_name = 'letterapp/saved.html'
    context_object_name = 'target_letter'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LetterIntroView(DetailView):
    model = Letter
    template_name = 'letterapp/intro.html'
    context_object_name = 'target_letter'

    def get(self, request, *args, **kwargs):
        target_letter = self.get_object()
        target_user = request.user
        if target_letter.is_received and not target_user in [target_letter.receiver, target_letter.sender]:
            return redirect('letterapp:expire')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['initial_letter'] = self.object.letter_quiz.all().order_by('created_at').first()
        return context


class LetterDetailView(DetailView):
    model = Letter
    template_name = 'letterapp/detail.html'
    context_object_name = 'target_letter'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['letter_content'] = self.object.letter_content
        context['letter_info'] = self.object.letter_info
        if self.request.user.is_authenticated:
            like = Letter_like.objects.filter(customuser=self.request.user, letter=self.object).first()
            context['like'] = like
        return context


class LetterExpireView(TemplateView):
    template_name = 'letterapp/expire.html'



@method_decorator(login_required, name='dispatch')
class LetterDeleteView(DeleteView):
    model = Letter
    context_object_name = 'target_letter'
    template_name = 'letterapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('accountapp:sentmailbox', kwargs={'pk': self.object.sender.pk})


@method_decorator(login_required, name='dispatch')
class LetterStateUpdateView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        letter = Letter.objects.get(pk=self.request.GET.get('letter_pk'))
        return reverse('letterapp:finish', kwargs={'pk': letter.pk})

    def get(self, request, *args, **kwargs):
        letter = Letter.objects.get(pk=self.request.GET.get('letter_pk'))
        with transaction.atomic():
            if letter.progress == 'progress3':
                letter.progress = 'done'
                letter.save()
            letter.finished_at = datetime.now()
            letter.save()

            return super(LetterStateUpdateView, self).get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class LetterSaveView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        letter = Letter.objects.get(pk=self.request.GET.get('letter_pk'))
        return reverse('letterapp:saved', kwargs={'pk': letter.pk})


    def get(self, request, *args, **kwargs):
        letter = Letter.objects.get(pk=self.request.GET.get('letter_pk'))
        with transaction.atomic():
            letter.receiver = self.request.user
            letter.is_received = True
            print('sdsd')
            letter.save()
            return super(LetterSaveView, self).get(request, *args, **kwargs)


class LetterSearchView(FormView):
    model = Letter
    template_name = 'letterapp/search.html'
    form_class = LetterSearchForm

    def get(self, request, *args, **kwargs):
        page_param = self.request.GET.get('page', None)
        if page_param:
            self.request.session["search_page"] =page_param
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.request.session["search_page"]
        return context

    def form_valid(self, form):
        target_user = self.request.user
        with transaction.atomic():
            self.target_letter_url = form.cleaned_data['letter_url']
            target_letter = Letter.objects.filter(url=self.target_letter_url, progress='done').first()
            if not target_letter:
                form.add_error('letter_url', '해당 링크의 편지가 없습니다.')
                return self.form_invalid(form)
            elif target_user == target_letter.sender:
                form.add_error('letter_url', '작성한 편지는 편지함에서 확인해요!')
                return self.form_invalid(form)
            elif target_user == target_letter.receiver:
                form.add_error('letter_url', '저장한 편지는 편지함에서 확인해요!')
                return self.form_invalid(form)
            return super().form_valid(form)

    def get_success_url(self):
        letter = Letter.objects.get(url=self.target_letter_url)
        return reverse('letterapp:intro', kwargs={'pk': letter.pk})
