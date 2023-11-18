from django.contrib.auth.views import LogoutView
from django.urls import path
from accountapp.views import *

app_name = 'accountapp'

urlpatterns = [
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('writelist/<uuid:pk>', AccountWriteListView.as_view(), name='writelist'),
    path('savelist/<uuid:pk>', AccountSaveListView.as_view(), name='savelist'),
    path('usernameupdate/<uuid:pk>', AccountUsernameUpdateView.as_view(), name='usernameupdate'),
    path('passwordupdate/<uuid:pk>', AccountPasswordUpdateView.as_view(), name='passwordupdate'),
    path('passwordreset/<uuid:pk>', AccountPasswordResetView.as_view(), name='passwordreset'),
    path('notificationupdate/', AccountNotificationUpdateView.as_view(), name='notificationupdate'),
    path('delete/<uuid:pk>', AccountDeleteView.as_view(), name='delete'),
    path('create/<uuid:pk>', AccountCreateView.as_view(), name='create'),
    path('setting/<uuid:pk>', AccountSettingView.as_view(), name='setting'),
]

