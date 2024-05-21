from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, RedirectView

from eventapp.models import Event


# Create your views here.
class EventDetailView(DetailView):
    model = Event
    template_name = 'eventapp/detail.html'
    context_object_name = 'event'

    def dispatch(self, request, *args, **kwargs):
        event=get_object_or_404(Event, pk=self.kwargs['pk'])
        if not event.can_read():
            return HttpResponseRedirect(reverse('eventapp:quiz', kwargs={'pk': event.pk}))
        event.count=0
        event.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventQuizView(DetailView):
    model = Event
    template_name = 'eventapp/quiz.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EventCatchView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('eventapp:detail', kwargs={'pk': self.request.GET.get('object_pk')})

    def get(self, request, *args, **kwargs):
        event = Event.objects.get(pk=request.GET.get('object_pk'))
        with transaction.atomic():
            event.count += 1
            event.save()
            return super(EventCatchView, self).get(request, *args, **kwargs)