# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_auto_20150716_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvedcourselist',
            name='elect_or_comp',
            field=models.IntegerField(default=1),
        ),
    ]
