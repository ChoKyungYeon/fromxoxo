from django.urls import path
from documentapp.views import DocumentUpdateView, DocumentCreateView

app_name = 'documentapp'

urlpatterns = [
    path('update/<uuid:pk>',DocumentUpdateView.as_view(), name='update'),
    path('create',DocumentCreateView.as_view(), name='create'),
]