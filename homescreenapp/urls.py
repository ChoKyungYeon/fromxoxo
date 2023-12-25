from django.urls import path

from homescreenapp.views import *

app_name = 'homescreenapp'

urlpatterns = [
    path('intro/', HomescreenIntroView.as_view(), name='intro'),
    path('event1/', HomescreenEvent1View.as_view(), name='event1'),
    path('event2/', HomescreenEvent2View.as_view(), name='event2'),
    path('event3/', HomescreenEvent3View.as_view(), name='event3'),
    path('event4/', HomescreenEvent4View.as_view(), name='event4'),
]