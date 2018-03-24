"""ETIMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from ets import views as core_views
from ets import views

urlpatterns = [
    path('', views.user_account, name='home'),
    path('direction/', views.direction_create, name='direction'),

    url(r'^profile/update/(?P<pk>[\-\w]+)/$', views.edit_user, name='profile/update'),
    path('profile/', views.my_profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^pay/(?P<id>\d+)/$', views.pay, name='pay'),  # view ticket payment
    url(r'^paid/(?P<uid>\d+)/(?P<id>\d+)/$', views.paid, name='paid'),  # payment callback


]
