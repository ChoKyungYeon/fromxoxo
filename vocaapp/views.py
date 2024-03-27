from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, RedirectView

from accountapp.models import CustomUser
from vocaapp.forms import VocaCreateForm
from vocaapp.models import Voca


class VocaListView(DetailView):
    model = CustomUser
    context_object_name = 'target_user'
    template_name = 'vocaapp/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vocas = self.object.voca.all()
        context['vocas'] = vocas
        context['vocas_liked'] = vocas.filter(is_liked=True)
        return context



class VocaCreateView(CreateView):
    model = Voca
    form_class = VocaCreateForm
    template_name = 'vocaapp/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.user = self.user
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('vocaapp:list', kwargs={'pk': self.object.user.pk})

class VocaUpdateView(UpdateView):
    model = Voca
    form_class = VocaCreateForm
    template_name = 'vocaapp/update.html'
    context_object_name = 'voca'

    def get_success_url(self):
        return reverse_lazy('vocaapp:list', kwargs={'pk': self.object.user.pk})
    
    
    
class VocaLikeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        voca = Voca.objects.get(pk=self.request.GET.get('object_pk'))
        return reverse('vocaapp:list', kwargs={'pk': voca.user.pk})

    def get(self, request, *args, **kwargs):
        voca = Voca.objects.get(pk=request.GET.get('object_pk'))
        with transaction.atomic():
            voca.is_liked = True if not voca.is_liked else False
            voca.save()
            return super(VocaLikeView, self).get(request, *args, **kwargs)