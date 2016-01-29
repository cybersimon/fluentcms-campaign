# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

from campaign.context import MailContext
from campaign.conf import settings


class BaseBackend(object):
    """Base backend for all campaign backends"""

    context_class = MailContext

    def send_campaign(self, campaign, fail_silently=False):
        from campaign.models import BlacklistEntry

        template = campaign.template
        from_email = self.get_from_email(campaign)
        current_site = Site.objects.get_current()

        num_sent = 0
        recipients = []
        for recipient_list in campaign.recipients.all():
            for recipient in recipient_list.object_list():
                email_address = getattr(recipient, recipient_list.email_field_name)

                if not bool(email_address):
                    continue

                if recipient in recipients:
                    continue

                if BlacklistEntry.objects.filter(email=email_address).count():
                    continue

                context = self.context_class(recipient).update({
                    'user': recipient if isinstance(recipient, get_user_model()) else None,
                    'campaign': campaign,
                })

                email_obj = template.get_email_message(
                    base_url=current_site.domain,
                    context=context,
                    to=[
                        email_address,
                    ],
                    from_email=from_email,
                )
                self.send_mail(email_obj, fail_silently)

                if recipient not in recipients:
                    recipients.append(recipient)
                num_sent += 1
        return num_sent

    def send_mail(self, email, fail_silently=False):
        raise NotImplementedError

    def get_from_email(self, campaign):
        from_email = settings.CAMPAIGN_FROM_EMAIL or settings.DEFAULT_FROM_EMAIL
        try:
            from_email = campaign.newsletter.from_email or from_email
        except:
            pass
        return from_email
