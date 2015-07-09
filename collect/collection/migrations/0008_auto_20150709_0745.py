# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0007_auto_20150709_0705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvedcourseteaching',
            name='elect_or_comp',
        ),
        migrations.AddField(
            model_name='approvedcourselist',
            name='elect_or_comp',
            field=models.IntegerField(default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='elect_or_comp',
            field=models.IntegerField(default=1, max_length=1),
            preserve_default=False,
        ),
    ]
