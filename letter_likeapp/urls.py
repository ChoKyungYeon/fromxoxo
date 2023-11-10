from django.urls import path

from letter_likeapp.views import *

app_name = 'letter_likeapp'

urlpatterns = [
    path('like/',Letter_likeView.as_view(), name='like'),
]