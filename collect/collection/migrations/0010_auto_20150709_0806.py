# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0009_auto_20150709_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foreigncourselist',
            name='credit',
            field=models.IntegerField(blank=True),
        ),
    ]
