# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0011_auto_20150709_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foreigncourselist',
            name='credit',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
