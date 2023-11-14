from django.urls import path

from homescreenapp.views import *

app_name = 'homescreenapp'

urlpatterns = [
    path('homescreen/', HomescreenView.as_view(), name='homescreen'),
    path('termofuse/', TermofuseView.as_view(), name='termofuse'),
    path('privacypolicy/', PrivacypolicyView.as_view(), name='privacypolicy'),
    path('announcement/', AnnouncementView.as_view(), name='announcement'),
    path('bugreport/', BugreportView.as_view(), name='bugreport'),
    path('createguide/', CreateGuideView.as_view(), name='createguide'),
]