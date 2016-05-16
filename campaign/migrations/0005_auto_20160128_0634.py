# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0004_newsletter_from_email'),
        ('fluentcms_emailtemplates', '__first__'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='template',
            field=models.ForeignKey(verbose_name='Template', to='fluentcms_emailtemplates.EmailTemplate'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='MailTemplate',
        ),
    ]
