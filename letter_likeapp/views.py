from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView
from django.utils.decorators import method_decorator

from letter_likeapp.decorators import Letter_likeDecorator
from letter_likeapp.models import Letter_like
from letterapp.models import Letter

@method_decorator(login_required, name='dispatch')
@method_decorator(Letter_likeDecorator, name='dispatch')
class Letter_likeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('letterapp:preview', kwargs={'pk': self.request.GET.get('object_pk')})

    def get(self, request, *args, **kwargs):
        target_user = request.user
        target_letter = get_object_or_404(Letter, pk=self.request.GET.get('object_pk'))
        letter_like = Letter_like.objects.filter(user=target_user, letter=target_letter)
        if letter_like.exists():
            letter_like.delete()
        else:
            Letter_like.objects.create(user=target_user, letter=target_letter)
        return super(Letter_likeView, self).get(request, *args, **kwargs)
