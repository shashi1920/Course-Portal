# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_auto_20150629_0639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvedcourseteaching',
            name='course',
        ),
    ]
