from django.db import transaction
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.core.files.base import ContentFile
from documentapp.models import Document
from letter_contentapp.models import Letter_content
from letter_infoapp.models import Letter_info
from letterapp.forms import LetterCreateForm


class HomescreenView(TemplateView):
    template_name = 'homescreenapp/homescreen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document'] = Document.objects.all().first()
        return context


class ContactView(TemplateView):
    template_name = 'homescreenapp/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document']=Document.objects.all().first()
        return context

    

class TermofuseView(TemplateView):
    template_name = 'homescreenapp/termofuse.html'

    def get(self, request, *args, **kwargs):
        document = Document.objects.all().first()
        if document.termofuse:
            return redirect(document.termofuse)
        return super().get(request, *args, **kwargs)

class AnnouncementView(TemplateView):
    template_name = 'homescreenapp/announcement.html'

    def get(self, request, *args, **kwargs):
        document = Document.objects.all().first()
        if document.announcement:
            return redirect(document.announcement)
        return super().get(request, *args, **kwargs)

class RefundView(TemplateView):
    template_name = 'homescreenapp/refund.html'


class PrivacypolicyView(TemplateView):
    template_name = 'homescreenapp/privacypolicy.html'

    def get(self, request, *args, **kwargs):
        document = Document.objects.all().first()
        if document.privacypolicy:
            return redirect(document.privacypolicy)
        return super().get(request, *args, **kwargs)

class CreateGuideView(TemplateView):
    template_name = 'homescreenapp/createguide.html'
    def get(self, request, *args, **kwargs):
        page_param=self.request.GET.get('page', None)
        if page_param:
            self.request.session["createguide_page"] = page_param
        return super().get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        target_user=self.request.user
        context = super().get_context_data(**kwargs)
        context['letter_form'] = LetterCreateForm()
        context['page'] = self.request.session.get("createguide_page", False)
        context['undone_letter'] =target_user.letter_sender.exclude(progress='done').first() if target_user.is_authenticated else None
        return context


    def post(self, request, *args, **kwargs):
        form = LetterCreateForm(request.POST, request.FILES)
        target_user = self.request.user
        if target_user.is_authenticated:
            if form.is_valid():
                with transaction.atomic():
                    target_user.letter_sender.exclude(progress='done').delete()
                    letter = form.save(commit=False)
                    letter.sender = target_user
                    letter.url = letter.generate_url()
                    letter.qr.save("letter_qrcode.png", ContentFile(letter.generate_qrcode(letter.url)))
                    letter.save()
                    Letter_content.objects.create(letter=letter)
                    letter_info = Letter_info.objects.create(letter=letter)
                    return redirect('letter_infoapp:update', pk=letter_info.pk)
