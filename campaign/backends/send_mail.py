# -*- coding: utf-8 -*-

from .base import BaseBackend


class SendMailBackend(BaseBackend):
    """
    Simple backend which uses Django's built-in mail sending mechanisms.

    If no sending address is specified in the database, the From-Email is
    determined from the following settings in this order::

        settings.CAMPAIGN_FROM_EMAIL  # used by all backends that support it
        settings.DEFAULT_FROM_EMAIL  # used by Django

    """
    def send_mail(self, email, fail_silently=False):
        return email.send(fail_silently=fail_silently)

backend = SendMailBackend()
