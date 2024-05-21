from django.urls import path
from eventapp.views import *

app_name = 'eventapp'

urlpatterns = [
    path('detail/<uuid:pk>', EventDetailView.as_view(), name='detail'),
    path('quiz/<uuid:pk>', EventQuizView.as_view(), name='quiz'),
    path('catch/', EventCatchView.as_view(), name='catch'),
]

