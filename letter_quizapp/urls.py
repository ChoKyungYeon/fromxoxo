from django.urls import path

from letter_quizapp.views import *

app_name = 'letter_quizapp'


urlpatterns = [
    path('create/<uuid:pk>', Letter_quizCreateView.as_view(), name='create'),
    path('update/<uuid:pk>', Letter_quizUpdateView.as_view(), name='update'),
    path('delete/<uuid:pk>', Letter_quizDeleteView.as_view(), name='delete'),
    path('list/<uuid:pk>', Letter_quizListView.as_view(), name='list'),
    path('verify/<uuid:pk>', Letter_quizVerifyView.as_view(), name='verify'),
]