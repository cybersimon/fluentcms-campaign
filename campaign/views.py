# -*- coding: utf-8 -*-

from django.utils import six
from django.conf import settings
from django.http import HttpResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic import FormView

import swapper
from parler.views import LanguageChoiceMixin

from fluentcms_emailtemplates.models import EmailTemplate
from fluentcms_emailtemplates.rendering import render_email_template

from .forms import SubscribeForm, UnsubscribeForm


Campaign = swapper.load_model("campaign", "Campaign")


class CampaignView(LanguageChoiceMixin, BaseDetailView):
    model = Campaign

    def get_queryset(self):
        return super(CampaignView, self).get_queryset().filter(online=True)

    def get_object(self):
        self.campaign = super(CampaignView, self).get_object()
        return self.campaign.template

    def get_context_data(self, **kwargs):
        context = super(CampaignView, self).get_context_data(**kwargs)

        extra_context = settings.FLUENTCMS_EMAILTEMPLATES_PREVIEW_CONTEXT
        if extra_context is None:
            extra_context = {}

        extra_context.update({'campaign': self.campaign})
        email = render_email_template(self.object,
            base_url=self.request.build_absolute_uri('/'),
            extra_context=extra_context,
            user=self.request.user,
        )
        context['email'] = email
        return context

    def render_to_response(self, context, **response_kwargs):
        # Allow fetching a raw HTML or text version.
        # Will render in the template otherwise.
        format = self.request.GET.get('format') or 'html'

        email = context['email']
        if format in ('text', 'txt'):
            return HttpResponse(six.text_type(
                email.text), content_type='text/plain; charset=utf8')
        return HttpResponse(six.text_type(
            email.html), content_type='text/html; charset=utf8')


class CampaignSubscribe(FormView):
    template_name = 'campaign/subscribe.html'
    form_class = SubscribeForm

    def form_valid(self, form):
        success = form.subscribe(request=self.request)
        return self.render_to_response(
            self.get_context_data(form=form, success=success, action='subscribe'))


class CampaignUnsubscribe(FormView):
    template_name = 'campaign/unsubscribe.html'
    form_class = UnsubscribeForm

    def form_valid(self, form):
        success = form.unsubscribe(request=self.request)
        return self.render_to_response(
            self.get_context_data(form=form, success=success, action='unsubscribe'))
