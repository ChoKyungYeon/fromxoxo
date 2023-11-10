from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from documentapp.decorators import *
from documentapp.forms import DocumentCreateForm
from documentapp.models import Document
from django.views.generic import UpdateView, CreateView

@method_decorator(login_required, name='dispatch')
@method_decorator(DocumentCreateDecorator, name='dispatch')
class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentCreateForm
    template_name = 'documentapp/create.html'
    def get_success_url(self):
        return reverse_lazy('superuserapp:sentmailbox')


@method_decorator(login_required, name='dispatch')
@method_decorator(DocumentCreateDecorator, name='dispatch')
class DocumentUpdateView(UpdateView):
    model = Document
    form_class = DocumentCreateForm
    context_object_name = 'target_document'
    template_name = 'documentapp/update.html'
    def get_success_url(self):
        return reverse_lazy('superuserapp:sentmailbox')


