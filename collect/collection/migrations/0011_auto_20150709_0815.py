# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0010_auto_20150709_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvedcourselist',
            name='elect_or_comp',
            field=models.IntegerField(default=1, max_length=1, blank=True),
        ),
        migrations.AlterField(
            model_name='foreigncourselist',
            name='elect_or_comp',
            field=models.IntegerField(default=1, max_length=1, blank=True),
        ),
    ]
