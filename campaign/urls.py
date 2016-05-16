# -*- coding: utf-8 -*-

from django.conf.urls import url

from .conf import settings
from .views import CampaignView

urlpatterns = [
    url(r'^view/(?P<pk>[\d]+)/$', CampaignView.as_view(), name='campaign_preview'),
]

if getattr(settings, 'CAMPAIGN_SUBSCRIBE_CALLBACK', None):
     from .views import CampaignSubscribe

     urlpatterns += [
         url(r'^subscribe/$', CampaignSubscribe.as_view(), name='campaign_subscribe'),
     ]

if getattr(settings, 'CAMPAIGN_UNSUBSCRIBE_CALLBACK', None):
     from .views import CampaignUnsubscribe

     urlpatterns += [
         url(r'^unsubscribe/$', CampaignUnsubscribe.as_view(), name='campaign_unsubscribe'),
     ]
