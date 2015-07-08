# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0004_auto_20150705_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='foreigncourselist',
            name='l',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='p',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='semester',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='t',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
