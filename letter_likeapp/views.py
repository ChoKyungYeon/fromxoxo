from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView
from django.utils.decorators import method_decorator

from letter_likeapp.models import Letter_like
from letterapp.models import Letter


@method_decorator(login_required, name='dispatch')
class Letter_likeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('letterapp:detail', kwargs={'pk':self.request.GET.get('letter_pk')})

    def get(self, request, *args, **kwargs):
        letter =get_object_or_404(Letter, pk=self.request.GET.get('letter_pk'))
        letter_like = Letter_like.objects.filter(customuser=self.request.user, letter=letter)
        if letter_like.exists():
            letter_like.delete()
        else:
            Letter_like.objects.create(customuser=self.request.user, letter=letter)
        return super(Letter_likeView, self).get(request, *args, **kwargs)


