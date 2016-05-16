# -*- coding: utf-8 -*-

import mandrill

from django.conf import settings
from django.core.management.base import NoArgsCommand

from campaign.models import BlacklistEntry


class Command(NoArgsCommand):
    """
    This command fetches all rejects from the Mandrill API and stores them
    in the local blacklist. This ensures that campaign doesn't send a mail to a
    bad recipient address more than once and that helps improving
    the deliverability rate.

    This command assumes that your Mandrill API-Key is configured in::

        settings.MANDRILL_API_KEY

    """
    help = "Fetch rejects from mandrill and store in local blacklist"

    def handle_noargs(self, **options):
        try:
            client = mandrill.Mandrill(settings.MANDRILL_API_KEY)

            for reject in client.rejects.list():
                if reject['reason'] in ('hard-bounce', 'spam', 'unsub'):
                     BlacklistEntry.objects.get_or_create(
                        email=reject['email'], defaults={
                            'reason': u"%s: %s" % (reject['reason'], reject['detail']),
                        })

        except mandrill.Error, e:
            raise e
