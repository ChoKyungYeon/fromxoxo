import uuid
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from letterapp.models import Letter

@method_decorator(never_cache, name='dispatch')
class HomescreenIntroView(TemplateView):
    template_name = 'homescreenapp/intro.html'

    def dispatch(self, request, *args, **kwargs):
        self.target_user = self.request.user
        self.ongoing_letter = None
        redirect_pk = self.request.session.get("redirect_pk", None)
        if self.target_user.is_authenticated:
            try:
                letter_uuid = uuid.UUID(redirect_pk)
                letter = Letter.objects.get(pk=letter_uuid)
                if not letter.is_user_related(self.target_user) and letter.state == 'checked':
                    self.ongoing_letter = letter
            except:
                pass
        self.request.session["redirect_pk"] = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ongoing_letter'] = self.ongoing_letter
        return context



