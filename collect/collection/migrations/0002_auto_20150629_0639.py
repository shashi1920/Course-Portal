# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dept',
            name='head',
            field=models.ForeignKey(to='collection.Profile', unique=True),
        ),
    ]
