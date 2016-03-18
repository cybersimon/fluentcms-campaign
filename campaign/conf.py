# -*- coding: utf-8 -*-

from django.conf import settings  # pylint: disable=W0611
from appconf import AppConf


class CampaignSettings(AppConf):
    BACKEND = 'campaign.backends.send_mail'
    FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
    CONTEXT_PROCESSORS = (
        'campaign.context_processors.recipient',
    )
    SUBSCRIBE_CALLBACK = None
    UNSUBSCRIBE_CALLBACK = None

    class Meta:
        prefix = 'campaign'
        holder = 'campaign.conf.settings'

