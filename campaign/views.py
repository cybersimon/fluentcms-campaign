# -*- coding: utf-8 -*-

from django.utils import six
from django.conf import settings
from django.http import HttpResponse
from django.views.generic.detail import BaseDetailView

from parler.views import LanguageChoiceMixin

from fluentcms_emailtemplates.models import EmailTemplate
from fluentcms_emailtemplates.rendering import render_email_template
# from django import template, http
# from django.shortcuts import get_object_or_404, render_to_response
# from django.core.urlresolvers import reverse
# from django.contrib.sites.models import Site

from .models import Campaign #, BlacklistEntry
# from .forms import SubscribeForm, UnsubscribeForm


class CampaignView(LanguageChoiceMixin, BaseDetailView):
    model = Campaign

    def get_queryset(self):
        return super(CampaignView, self).get_queryset().filter(online=True)

    def get_object(self):
        obj = super(CampaignView, self).get_object()
        return obj.template

    def get_context_data(self, **kwargs):
        context = super(CampaignView, self).get_context_data(**kwargs)
        email = render_email_template(self.object,
            base_url=self.request.build_absolute_uri('/'),
            extra_context=settings.FLUENTCMS_EMAILTEMPLATES_PREVIEW_CONTEXT,
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


# def subscribe(request, template_name='campaign/subscribe.html',
#               form_class=SubscribeForm, extra_context=None):
#     context = extra_context or {}
#     if request.method == 'POST':
#         form = form_class(request.POST)
#         if form.is_valid():
#             callback = _get_callback('CAMPAIGN_SUBSCRIBE_CALLBACK')
#             if callback:
#                 success = callback(form.cleaned_data['email'])
#                 context.update({'success': success, 'action': 'subscribe'})
#             else:
#                 raise ImproperlyConfigured("CAMPAIGN_SUBSCRIBE_CALLBACK must be configured to use the subscribe view")
#     else:
#         form = form_class()
#     context.update({'form': form})
#     return render_to_response(template_name, context,
#                         context_instance=template.RequestContext(request))


# def unsubscribe(request, template_name='campaign/unsubscribe.html',
#                 form_class=UnsubscribeForm, extra_context=None):
#     context = extra_context or {}
#     if request.method == 'POST':
#         form = form_class(request.POST)
#         if form.is_valid():
#             callback = _get_callback('CAMPAIGN_UNSUBSCRIBE_CALLBACK')
#             if callback:
#                 success = callback(form.cleaned_data['email'])
#                 context.update({'success': success, 'action': 'unsubscribe'})
#             else:
#                 raise ImproperlyConfigured("CAMPAIGN_UNSUBSCRIBE_CALLBACK must be configured to use the unsubscribe view")
#     else:
#         initial = {}
#         if request.GET.get('email'):
#             initial['email'] = request.GET.get('email')
#         form = form_class(initial=initial)
#     context.update({'form': form})
#     return render_to_response(template_name, context,
#                         context_instance=template.RequestContext(request))


# def _get_callback(setting):
#     callback = getattr(settings, setting, None)
#     if callback is None:
#         return None
#     if callable(callback):
#         return callback
#     else:
#         mod, name = callback.rsplit('.', 1)
#         module = __import__(mod, {}, {}, [''])
#         return getattr(module, name)
