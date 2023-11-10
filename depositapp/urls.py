from django.urls import path
from depositapp.views import DepositUpdateView, DepositCreateView

app_name = 'depositapp'

urlpatterns = [
    path('update/<uuid:pk>',DepositUpdateView.as_view(), name='update'),
    path('create',DepositCreateView.as_view(), name='create'),
]