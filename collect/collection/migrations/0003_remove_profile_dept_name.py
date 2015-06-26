# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_auto_20150626_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='dept_name',
        ),
    ]
