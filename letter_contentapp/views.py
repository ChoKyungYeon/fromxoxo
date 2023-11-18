from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import UpdateView

from letter_contentapp.decorators import Letter_contentUpdateDecorator
from letter_contentapp.forms import *
from letter_contentapp.models import Letter_content

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Letter_contentUpdateDecorator, name='dispatch')
class Letter_contentUpdateView(UpdateView):
    model = Letter_content
    form_class = Letter_contentCreateForm
    template_name = 'letter_contentapp/update.html'
    context_object_name = 'target_content'

    def dispatch(self, request, *args, **kwargs):
        self.target_letter=self.get_object().letter
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        progress= self.target_letter.progress
        with transaction.atomic():
            self.target_letter.progress = 'progress3' if progress == 'progress2' else progress
            self.target_letter.save()
            form.instance.save()
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_letter'] = self.target_letter
        context['tema'] = self.object.tema
        return context


    def get_success_url(self):
        return reverse_lazy('letter_quizapp:list', kwargs={'pk': self.target_letter.pk})



