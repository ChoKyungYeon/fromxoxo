from django.urls import path
from vocaapp.views import *

app_name = 'vocaapp'

urlpatterns = [
    path('list/<uuid:pk>', VocaListView.as_view(), name='list'),
    path('like/', VocaLikeView.as_view(), name='like'),
    path('create/<uuid:pk>', VocaCreateView.as_view(), name='create'),
    path('update/<uuid:pk>', VocaUpdateView.as_view(), name='update'),
]

