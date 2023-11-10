from django.urls import path

from homescreenapp.views import *

app_name = 'homescreenapp'

urlpatterns = [
    path('homescreen/', HomescreenView.as_view(), name='homescreen'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('termofuse/', TermofuseView.as_view(), name='termofuse'),
    path('refund/', RefundView.as_view(), name='refund'),
    path('privacypolicy/', PrivacypolicyView.as_view(), name='privacypolicy'),
    path('announcement/', AnnouncementView.as_view(), name='announcement'),
    path('createguide/', CreateGuideView.as_view(), name='createguide'),
]