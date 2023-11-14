from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, TemplateView
from accountapp.models import CustomUser
from django.utils.decorators import method_decorator
from letterapp.models import Letter
from letter_contentapp.forms import *
from letter_contentapp.models import Letter_content



@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class Letter_contentUpdateView(UpdateView):
    model = Letter_content
    form_class = Letter_contentCreateForm
    template_name = 'letter_contentapp/update.html'
    context_object_name = 'target_content'

    def form_valid(self, form):
        target_letter=self.object.letter
        with transaction.atomic():
            form.instance.save()
            if target_letter.progress == 'progress2':
                target_letter.progress = 'progress3'
                target_letter.save()
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_letter'] = self.object.letter
        context['progress'] = 2
        context['tema'] = self.object.tema
        return context


    def get_success_url(self):
        return reverse_lazy('letter_quizapp:list', kwargs={'pk': self.object.letter.pk})


@method_decorator(login_required, name='dispatch')
class Letter_contentDeleteView(DeleteView):
    model = Letter_content
    context_object_name = 'target_letter_content'
    template_name = 'letter_contentapp/delete.html'
    def get_success_url(self):
        return reverse_lazy('accountapp:sentmailbox')


