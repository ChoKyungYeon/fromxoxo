from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import UpdateView

from letter_infoapp.decorators import Letter_infoUpdateDecorator
from letter_infoapp.forms import *
from letter_infoapp.models import Letter_info

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Letter_infoUpdateDecorator, name='dispatch')
class Letter_infoUpdateView(UpdateView):
    model = Letter_info
    form_class = Letter_infoCreateForm
    template_name = 'letter_infoapp/update.html'
    context_object_name = 'target_info'

    def dispatch(self, request, *args, **kwargs):
        self.target_letter=self.get_object().letter
        self.target_content=self.target_letter.letter_content
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_letter'] = self.target_letter
        context['tema'] = self.target_content.tema
        return context

    def form_valid(self, form):
        written_at = form.cleaned_data['written_at']
        progress = self.target_letter.progress
        with transaction.atomic():
            if written_at > datetime.now().date():
                form.add_error('written_at', '오늘보다 큰 날짜는 설정이 불가능해요!')
                return self.form_invalid(form)

            self.target_letter.progress = 'progress2' if progress == 'progress1' else progress
            self.target_letter.save()

            form.instance.save()
            return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('letter_contentapp:update', kwargs={'pk': self.target_content.pk})



