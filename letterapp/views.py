from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import DetailView, DeleteView, TemplateView, RedirectView, FormView, CreateView
from fromxoxo.utils import register_session, is_user_related
from letter_contentapp.models import Letter_content
from letter_infoapp.models import Letter_info
from letter_likeapp.models import Letter_like
from letterapp.decorators import *
from letterapp.forms import *
from letterapp.models import Letter


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='post')
class LetterCreateView(CreateView):
    model = Letter
    form_class = LetterCreateForm
    template_name = 'letterapp/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.target_user = request.user
        register_session(self, 'from')
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from'] = self.request.session.get("from", None)
        context['undone_letter'] = self.target_user.letter_writer.exclude(
            progress='done').first() if self.target_user.is_authenticated else None
        return context


    def form_valid(self, form):
        with transaction.atomic():
            self.target_user.letter_writer.exclude(progress='done').delete()
            form.instance.writer = self.target_user
            form.instance.url = form.instance.generate_url()
            form.instance.qr.save("letter_qrcode.png", ContentFile(form.instance.generate_qrcode(form.instance.url)))
            Letter_content.objects.create(letter=form.instance)
            Letter_info.objects.create(letter=form.instance)
            form.instance.save()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('letter_infoapp:update', kwargs={'pk': self.object.letter_info.pk})

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(LetterResultDecorator, name='dispatch')
class LetterResultView(DetailView):
    model = Letter
    template_name = 'letterapp/result.html'
    context_object_name = 'target_letter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from'] = self.request.GET.get('from', None)
        context['tema'] = self.object.letter_content.tema
        return context


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(LetterFinishDecorator, name='dispatch')
class LetterFinishView(DetailView):
    model = Letter
    template_name = 'letterapp/finish.html'
    context_object_name = 'target_letter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = self.object.letter_content.tema
        return context

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(LetterSavedDecorator, name='dispatch')
class LetterSavedView(DetailView):
    model = Letter
    template_name = 'letterapp/saved.html'
    context_object_name = 'target_letter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = self.object.letter_content.tema
        return context


class LetterExpireView(TemplateView):
    template_name = 'letterapp/expire.html'

    def dispatch(self, request, *args, **kwargs):
        self.type = request.GET.get('type', None)
        if not self.type or self.type not in ['none','saved']:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.type
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(LetterDeleteDecorator, name='dispatch')
class LetterDeleteView(DeleteView):
    model = Letter
    context_object_name = 'target_letter'
    template_name = 'letterapp/delete.html'

    def get_success_url(self):
        return reverse_lazy('accountapp:writelist', kwargs={'pk': self.object.writer.pk})


@method_decorator(login_required, name='dispatch')
@method_decorator(LetterProgressUpdateDecorator, name='dispatch')
class LetterProgressUpdateView(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        self.target_letter =Letter.objects.get(pk=self.request.GET.get('letter_pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('letterapp:finish', kwargs={'pk': self.target_letter.pk})

    def get(self, request, *args, **kwargs):
        progress = self.target_letter.progress
        with transaction.atomic():
            self.target_letter.progress = 'done' if progress == 'progress3' else progress
            self.target_letter.finished_at = datetime.now()
            self.target_letter.save()
            return super(LetterProgressUpdateView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(LetterSaveDecorator, name='dispatch')
class LetterSaveView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('letterapp:saved', kwargs={'pk': self.request.GET.get('letter_pk')})

    def get(self, request, *args, **kwargs):
        target_letter = Letter.objects.get(pk=request.GET.get('letter_pk'))
        with transaction.atomic():
            target_letter.saver = request.user
            target_letter.state = 'saved'
            target_letter.expire_from = None
            target_letter.is_unsaved = False
            target_letter.save()
            return super(LetterSaveView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(LetterUnsaveDecorator, name='dispatch')
class LetterUnsaveView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accountapp:savelist', kwargs={'pk': self.request.user.pk})

    def get(self, request, *args, **kwargs):
        target_letter = Letter.objects.get(pk=request.GET.get('letter_pk'))
        with transaction.atomic():
            target_letter.saver = None
            target_letter.state = 'checked'
            target_letter.expire_from = datetime.now()
            target_letter.is_unsaved = True
            target_letter.save()
            return super(LetterUnsaveView, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(LetterResetDecorator, name='dispatch')
class LetterResetView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('letterapp:result', kwargs={'pk': self.request.GET.get('letter_pk')})

    def get(self, request, *args, **kwargs):
        target_letter = Letter.objects.get(pk=request.GET.get('letter_pk'))
        with transaction.atomic():
            target_letter.expire_from = None
            target_letter.state = 'unchecked'
            target_letter.save()
            return super(LetterResetView, self).get(request, *args, **kwargs)

@method_decorator(never_cache, name='dispatch')
class LetterSearchView(FormView):
    model = Letter
    template_name = 'letterapp/search.html'
    form_class = LetterSearchForm

    def dispatch(self, request, *args, **kwargs):
        register_session(self,'from')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from'] = self.request.session.get("from", None)
        context['tema'] = 'blue'
        return context

    def form_valid(self, form):
        target_user = self.request.user
        url = form.cleaned_data['url']
        self.target_letter = Letter.objects.filter(url=url, progress='done').first()
        with transaction.atomic():
            if not url.startswith('https://tinyurl.com/'):
                form.add_error('url', '편지의 링크 형식이 아니에요!')
                return self.form_invalid(form)

            elif not self.target_letter:
                form.add_error('url', '해당 링크의 편지가 없습니다.')
                return self.form_invalid(form)

            elif target_user == self.target_letter.writer:
                form.add_error('url', '작성한 편지는 편지함에서 확인해요!')
                return self.form_invalid(form)

            elif target_user == self.target_letter.saver:
                form.add_error('url', '저장한 편지는 편지함에서 확인해요!')
                return self.form_invalid(form)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('letterapp:intro', kwargs={'pk': self.target_letter.pk})


@method_decorator(never_cache, name='dispatch')
@method_decorator(LetterIntroDecorator, name='dispatch')
class LetterIntroView(DetailView):
    model = Letter
    template_name = 'letterapp/intro.html'
    context_object_name = 'target_letter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = self.object.letter_content.tema
        context['page'] = 'intro'
        return context


@method_decorator(never_cache, name='dispatch')
@method_decorator(LetterDetailDecorator, name='dispatch')
class LetterDetailView(DetailView):
    model = Letter
    template_name = 'letterapp/detail.html'
    context_object_name = 'target_letter'

    def dispatch(self, request, *args, **kwargs):
        self.target_user = request.user
        target_letter= get_object_or_404(Letter, pk=self.kwargs['pk'])
        if target_letter.state == 'unchecked':
            target_letter.state = 'checked'
            target_letter.expire_from = datetime.now()
            target_letter.save()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['letter_content'] = self.object.letter_content
        context['letter_info'] = self.object.letter_info
        context['tema'] = self.object.letter_content.tema
        return context


@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(LetterPreviewDecorator, name='dispatch')
class LetterPreviewView(DetailView):
    model = Letter
    template_name = 'letterapp/preview.html'
    context_object_name = 'target_letter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['letter_content'] = self.object.letter_content
        context['letter_info'] = self.object.letter_info
        context['tema'] = self.object.letter_content.tema
        context['like'] = Letter_like.objects.filter(user=self.request.user, letter=self.object).first()
        return context
