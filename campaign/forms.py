# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ImproperlyConfigured

from .conf import settings
from .utils import import_callback


class SubscribeForm(forms.Form):

    email = forms.EmailField()

    def subscribe(self, request):
        callback = import_callback(settings.CAMPAIGN_SUBSCRIBE_CALLBACK)
        if callback is None:
            raise ImproperlyConfigured(
                "CAMPAIGN_SUBSCRIBE_CALLBACK must be configured to use the subscribe form")

        return callback(self.cleaned_data['email'])


class UnsubscribeForm(forms.Form):

    email = forms.EmailField()

    def unsubscribe(self, request):
        callback = import_callback(settings.CAMPAIGN_UNSUBSCRIBE_CALLBACK)
        if callback is None:
            raise ImproperlyConfigured(
                "CAMPAIGN_UNSUBSCRIBE_CALLBACK must be configured to use the unsubscribe form")

        return callback(self.cleaned_data['email'])
