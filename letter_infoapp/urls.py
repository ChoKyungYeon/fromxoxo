from django.urls import path

from letter_infoapp.views import *

app_name = 'letter_infoapp'


urlpatterns = [
    path('update/<uuid:pk>', Letter_infoUpdateView.as_view(), name='update'),
]