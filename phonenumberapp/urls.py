from phonenumberapp.views import *
from django.urls import path


app_name = 'phonenumberapp'

urlpatterns = [
    path('create/',PhonenumberCreateView.as_view(), name='create'),
    path('verify/<uuid:pk>',PhonenumberVerifyView.as_view(), name='verify'),
]
