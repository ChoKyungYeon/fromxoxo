from django.urls import path

from letterapp.views import *

app_name = 'letterapp'

urlpatterns = [
    path('detail/<uuid:pk>', LetterDetailView.as_view(), name='detail'),
    path('result/<uuid:pk>', LetterResultView.as_view(), name='result'),
    path('saveinfo/<uuid:pk>', LetterSaveinfoView.as_view(), name='saveinfo'),
    path('intro/<uuid:pk>', LetterIntroView.as_view(), name='intro'),
    path('finish/<uuid:pk>', LetterFinishView.as_view(), name='finish'),
    path('saved/<uuid:pk>', LetterSavedView.as_view(), name='saved'),
    path('expire/', LetterExpireView.as_view(), name='expire'),
    path('delete/<uuid:pk>', LetterDeleteView.as_view(), name='delete'),
    path('delete/<uuid:pk>', LetterDeleteView.as_view(), name='delete'),
    path('stateupdate/', LetterStateUpdateView.as_view(), name='stateupdate'),
    path('save/', LetterSaveView.as_view(), name='save'),
    path('search/', LetterSearchView.as_view(), name='search'),
]