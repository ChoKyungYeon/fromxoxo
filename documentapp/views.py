from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import TemplateView

from documentapp.models import Document


class DocumentOpenView(TemplateView):
    template_name = 'documentapp/detail.html'

    def dispatch(self, request, *args, **kwargs):
        type = request.GET.get('type', None)
        target_document = Document.objects.all().first()
        if not type or type not in ['bugreport','termofuse','privacypolicy','announcement']:
            return HttpResponseForbidden()

        if not target_document:
            return HttpResponseForbidden()

        if type == 'bugreport':
            redirect_url = target_document.bugreport
        elif type == 'termofuse':
            redirect_url = target_document.termofuse
        elif type == 'privacypolicy':
            redirect_url = target_document.privacypolicy
        else:
            redirect_url = target_document.announcement
        return HttpResponseRedirect(redirect_url) if redirect_url else HttpResponseForbidden()
