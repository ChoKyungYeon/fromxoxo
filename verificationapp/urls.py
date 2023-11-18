from verificationapp.views import *
from django.urls import path


app_name = 'verificationapp'

urlpatterns = [
    path('create/',VerificationCreateView.as_view(), name='create'),
    path('verify/<uuid:pk>',VerificationVerifyView.as_view(), name='verify'),
]
