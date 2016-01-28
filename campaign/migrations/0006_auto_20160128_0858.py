# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0005_auto_20160128_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campaign',
            name='newsletter',
            field=models.ForeignKey(verbose_name='newsletter', blank=True, to='campaign.Newsletter', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campaign',
            name='recipients',
            field=models.ManyToManyField(to='campaign.SubscriberList', verbose_name='subscriber lists'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campaign',
            name='template',
            field=models.ForeignKey(verbose_name='template', to='fluentcms_emailtemplates.EmailTemplate'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='description',
            field=models.TextField(null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='from_email',
            field=models.EmailField(max_length=75, null=True, verbose_name='sending address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscriberlist',
            name='email_field_name',
            field=models.CharField(help_text='Name of the model field which stores the recipients email address', max_length=64, verbose_name='EmailField name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscriberlist',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
            preserve_default=True,
        ),
    ]
