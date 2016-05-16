fluentcms-campaign
==================

fluentcms-campaign is a newsletter campaign management app, that uses
django-fluent-contents_ blocks to define the e-mail templates.

.. image:: https://img.shields.io/pypi/v/fluentcms-campaign.svg
    :target: https://pypi.python.org/pypi/fluentcms-campaign/

.. image:: https://img.shields.io/pypi/dm/fluentcms-campaign.svg
    :target: https://pypi.python.org/pypi/fluentcms-campaign/

.. image:: https://img.shields.io/github/license/bashu/fluentcms-campaign.svg
    :target: https://pypi.python.org/pypi/fluentcms-campaign/


Installation
============

First install the module, preferably in a virtual environment. It can be installed from PyPI:

.. code-block:: shell

    pip install fluentcms-campaign


Backend Configuration
---------------------

First make sure the project is configured for fluentcms-emailtemplates_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'campaign',
    )

Update your urls.py file:

.. code-block:: python

    urlpatterns += [
        url(r'^campaign/', include('campaign.urls')),
    ]

The database tables can be created afterwards:

.. code-block:: shell

    python ./manage.py migrate

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _django-campaign: https://github.com/arneb/django-campaign
.. _django-fluent-contents: https://github.com/edoburu/django-fluent-contents
.. _fluentcms-emailtemplates: https://github.com/edoburu/fluentcms-emailtemplates
