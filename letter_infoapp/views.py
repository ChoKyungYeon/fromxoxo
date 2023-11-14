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
from letter_infoapp.forms import *
from letter_infoapp.models import Letter_info




@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class Letter_infoUpdateView(UpdateView):
    model = Letter_info
    form_class = Letter_infoCreateForm
    template_name = 'letter_infoapp/update.html'
    context_object_name = 'target_info'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_letter=self.object.letter
        context['target_letter'] = target_letter
        context['progress'] = 1
        context['tema'] = target_letter.letter_content.tema
        return context

    def form_valid(self, form):
        written_at = form.cleaned_data['written_at']
        target_letter=self.object.letter
        with transaction.atomic():
            if written_at > datetime.now().date():
                form.add_error('written_at', '오늘보다 큰 날짜는 설정이 불가능해요!')
                return self.form_invalid(form)
            form.instance.save()
            if target_letter.progress == 'progress1':
                target_letter.progress = 'progress2'
                target_letter.save()
            return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('letter_contentapp:update', kwargs={'pk': self.object.letter.letter_content.pk})



