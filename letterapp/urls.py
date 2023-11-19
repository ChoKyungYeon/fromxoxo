from django.urls import path

from letterapp.views import *

app_name = 'letterapp'

urlpatterns = [
    path('detail/<uuid:pk>', LetterDetailView.as_view(), name='detail'),
    path('preview/<uuid:pk>', LetterPreviewView.as_view(), name='preview'),
    path('result/<uuid:pk>', LetterResultView.as_view(), name='result'),
    path('intro/<uuid:pk>', LetterIntroView.as_view(), name='intro'),
    path('finish/<uuid:pk>', LetterFinishView.as_view(), name='finish'),
    path('saved/<uuid:pk>', LetterSavedView.as_view(), name='saved'),
    path('expire/', LetterExpireView.as_view(), name='expire'),
    path('delete/<uuid:pk>', LetterDeleteView.as_view(), name='delete'),
    path('delete/<uuid:pk>', LetterDeleteView.as_view(), name='delete'),
    path('progressupdate/', LetterProgressUpdateView.as_view(), name='progressupdate'),
    path('save/', LetterSaveView.as_view(), name='save'),
    path('unsave/', LetterUnsaveView.as_view(), name='unsave'),
    path('reset/', LetterResetView.as_view(), name='reset'),
    path('search/', LetterSearchView.as_view(), name='search'),
    path('create/', LetterCreateView.as_view(), name='create'),
]