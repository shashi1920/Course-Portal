# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0013_checklist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='programme_code',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='programme',
            name='programme_name',
            field=models.CharField(max_length=250),
        ),
    ]
