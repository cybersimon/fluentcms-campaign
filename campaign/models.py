# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

import swapper

from .fields import JSONField
from .abstracts import CampaignAbstract
from .backends import get_backend


class Newsletter(models.Model):
    """
    Represents a recurring newsletter which users can subscribe to.

    """
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    from_email = models.EmailField(_("sending address"), blank=True, null=True)

    class Meta:
        verbose_name = _("newsletter")
        verbose_name_plural = _("newsletters")
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class SubscriberList(models.Model):
    """
    A pointer to another Django model which holds the subscribers.

    """
    name = models.CharField(_("name"), max_length=255)
    content_type = models.ForeignKey(ContentType)
    filter_condition = JSONField(default="{}",
        help_text=_("Django ORM compatible lookup kwargs which are used to get the list of objects."))
    email_field_name = models.CharField(_("EmailField name"), max_length=64,
        help_text=_("Name of the model field which stores the recipients email address"))

    class Meta:
        verbose_name = _("subscriber list")
        verbose_name_plural = _("subscriber lists")
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def _get_filter(self):
        # simplejson likes to put unicode objects as dictionary keys
        # but keyword arguments must be str type
        fc = {}
        for k,v in self.filter_condition.iteritems():
            fc.update({str(k): v})
        return fc

    def object_list(self):
        return self.content_type.model_class()._default_manager.filter(
            **self._get_filter())

    def object_count(self):
        return self.object_list().count()


class Campaign(CampaignAbstract):
    """
    A Campaign is the central part of this app. Once a Campaign is
    created, has a MailTemplate and one or more SubscriberLists, it
    can be send out.  Most of the time of Campain will have a
    one-to-one relationship with a MailTemplate, but templates may be
    reused in other Campaigns and maybe Campaigns will have support
    for multiple templates in the future, therefore the distinction.

    A Campaign optionally belongs to a Newsletter.

    """

    class Meta(CampaignAbstract.Meta):
        abstract = False
        swappable = swapper.swappable_setting('campaign', 'Campaign')


class BlacklistEntry(models.Model):
    """
    If a user has requested removal from the subscriber-list, he is
    added to the blacklist to prevent accidential adding of the same
    user again on subsequent imports from a data source.

    """
    email = models.EmailField()
    added = models.DateTimeField(default=timezone.now, editable=False)
    reason = models.TextField(_("reason"), blank=True, null=True)

    class Meta:
        verbose_name = _("blacklist entry")
        verbose_name_plural = _("blacklist entries")
        ordering = ('-added',)

    def __unicode__(self):
        return self.email
