# -*- coding: utf-8 -*-

from functools import update_wrapper

from django.contrib import admin
from django.contrib import messages
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.contrib.admin.utils import quote, unquote
try:
    from django.utils.encoding import force_unicode as force_text
except ImportError:
    from django.utils.encoding import force_text
from django.contrib.admin.options import IS_POPUP_VAR
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.utils.html import escape

import swapper

from .models import Campaign, BlacklistEntry, SubscriberList, Newsletter

admin.site.register(SubscriberList)
admin.site.register(Newsletter, list_display=('name', 'from_email'))


class CampaignAdmin(admin.ModelAdmin):
    filter_horizontal=('recipients',)
    list_display=('name', 'newsletter', 'sent', 'sent_at', 'online')
    change_form_template = 'admin/campaign/campaign/change_form.html'
    send_template = None

    def has_send_permission(self, request, obj):
        """
        Subclasses may override this and implement more granular permissions.
        """
        return request.user.has_perm('campaign.send_campaign')

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        urlpatterns = [
            url(r'^(.+)/send/$', wrap(self.send_view), name='%s_%s_send' % info),
        ]
        return urlpatterns + super(CampaignAdmin, self).get_urls()

    def send_view(self, request, object_id, extra_context=None):
        """
        Allows the admin to send out the mails for this campaign.
        """
        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id))

        if not self.has_send_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': force_text(model._meta.verbose_name),
                'key': escape(object_id),
            })

        if request.method == 'POST':
            if not request.POST.get('action', None) == 'send':
                raise PermissionDenied

            num_sent = obj.send()

            self.message_user(request,
                _('The %(name)s "%(obj)s" was successfully sent. %(num_sent)s messages delivered.' %  {
                    'name': force_text(opts.verbose_name),
                    'obj': force_text(obj),
                    'num_sent': num_sent,
                }), messages.SUCCESS)
            return HttpResponseRedirect(reverse(
                'admin:%s_%s_change' % (opts.app_label, opts.model_name),
                args=(quote(obj._get_pk_val()),),
                current_app=self.admin_site.name,
            ))

        context = dict(
            title=_('Send %s') % force_text(opts.verbose_name),
            object_id=object_id,
            object=obj,
            is_popup=(IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
            media=self.media,
            app_label=opts.app_label,
            opts=opts,
        )
        context.update(extra_context or {})

        return TemplateResponse(request,
            self.send_template or [
                'admin/%s/%s/send_object.html' % (opts.app_label, opts.object_name.lower()),
                'admin/%s/send_object.html' % opts.app_label,
                'admin/send_object.html',
            ], context)

if not swapper.is_swapped('campaign', 'Campaign'):
    admin.site.register(Campaign, CampaignAdmin)


class BlacklistEntryAdmin(admin.ModelAdmin):
    list_display=('email', 'added')

admin.site.register(BlacklistEntry, BlacklistEntryAdmin)
