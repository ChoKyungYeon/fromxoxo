from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from depositapp.decorators import *
from depositapp.forms import DepositCreateForm
from depositapp.models import Deposit
from django.views.generic import UpdateView, CreateView

@method_decorator(login_required, name='dispatch')
@method_decorator(DepositCreateDecorator, name='dispatch')
class DepositCreateView(CreateView):
    model = Deposit
    form_class = DepositCreateForm
    template_name = 'depositapp/create.html'
    def get_success_url(self):
        return reverse_lazy('superuserapp:sentmailbox')


@method_decorator(login_required, name='dispatch')
@method_decorator(DepositCreateDecorator, name='dispatch')
class DepositUpdateView(UpdateView):
    model = Deposit
    form_class = DepositCreateForm
    context_object_name = 'target_deposit'
    template_name = 'depositapp/update.html'
    def get_success_url(self):
        return reverse_lazy('superuserapp:sentmailbox')


