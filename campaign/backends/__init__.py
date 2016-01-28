# -*- coding: utf-8 -*-

import os
import warnings

from django.core.exceptions import ImproperlyConfigured

from campaign.conf import settings


def get_backend(import_path=settings.CAMPAIGN_BACKEND):
    if not '.' in import_path:
        warnings.warn("CAMPAIGN_BACKEND should be a fully qualified module name",
            DeprecationWarning)
        import_path = "campaign.backends.%s" % import_path
    try:
        mod = __import__(import_path, {}, {}, [''])
    except ImportError, e_user:
        # No backend found, display an error message and a list of all
        # bundled backends.
        backends = [f.split('.py')[0] for f in os.listdir(__path__[0]) if not f.startswith('_') and not f.startswith('.') and not f.endswith('.pyc')]
        backends.sort()
        if settings.CAMPAIGN_BACKEND not in backends:
            raise ImproperlyConfigured("%s isn't an available campaign backend. Available options are: %s" % (
                settings.CAMPAIGN_BACKEND, ', '.join(map(repr, backends))))
        # If the CAMPAIGN_BACKEND is available in the backend
        # directory and an ImportError is raised, don't suppress it
        else: 
            raise
    try:
        return getattr(mod, 'backend')
    except AttributeError:
        raise ImproperlyConfigured('Backend "%s" does not define a "backend" instance.' % import_path)

backend = get_backend(settings.CAMPAIGN_BACKEND)
