from django.urls import path

from homescreenapp.views import *

app_name = 'homescreenapp'

urlpatterns = [
    path('intro/', HomescreenIntroView.as_view(), name='intro'),
]