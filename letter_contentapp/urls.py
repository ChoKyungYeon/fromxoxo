from django.urls import path

from letter_contentapp.views import *

app_name = 'letter_contentapp'


urlpatterns = [
    path('update/<uuid:pk>', Letter_contentUpdateView.as_view(), name='update'),
    path('save/<uuid:pk>', Letter_contentSaveView.as_view(), name='save'),
]