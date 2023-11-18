from django.urls import path

from documentapp.views import DocumentOpenView

app_name = 'documentapp'

urlpatterns = [
    path('open/', DocumentOpenView.as_view(), name='open'),
]