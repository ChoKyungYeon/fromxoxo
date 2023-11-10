from django.contrib.auth.views import LogoutView
from django.urls import path
from accountapp.views import *

app_name = 'accountapp'

urlpatterns = [
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sentmailbox/<uuid:pk>', AccountSentMailboxView.as_view(), name='sentmailbox'),
    path('savedmailbox/<uuid:pk>', AccountSavedMailboxView.as_view(), name='savedmailbox'),
    path('usernameupdate/<uuid:pk>', AccountUsernameUpdateView.as_view(), name='usernameupdate'),
    path('passwordupdate/<uuid:pk>', AccountPasswordUpdateView.as_view(), name='passwordupdate'),
    path('reset/<uuid:pk>', AccountResetView.as_view(), name='reset'),
    path('notificationupdate/', AccountNotificationUpdateView.as_view(), name='notificationupdate'),
    path('delete/<uuid:pk>', AccountDeleteView.as_view(), name='delete'),
    path('create/<uuid:pk>', AccountCreateView.as_view(), name='create'),
    path('setting/<uuid:pk>', AccountSettingView.as_view(), name='setting'),
]

