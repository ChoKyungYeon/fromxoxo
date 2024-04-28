"""basicframe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-ba sed views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='homescreens/intro', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accountapp.urls')),
    path('homescreens/', include('homescreenapp.urls')),
    path('verifications/', include('verificationapp.urls')),
    path('letters/', include('letterapp.urls')),
    path('letter_quizs/', include('letter_quizapp.urls')),
    path('letter_contents/', include('letter_contentapp.urls')),
    path('letter_infos/', include('letter_infoapp.urls')),
    path('letter_likes/', include('letter_likeapp.urls')),
    path('documents/', include('documentapp.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

