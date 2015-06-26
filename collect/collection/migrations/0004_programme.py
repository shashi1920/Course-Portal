# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_remove_profile_dept_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='programme',
            fields=[
                ('programme_code', models.CharField(max_length=5, serialize=False, primary_key=True)),
                ('programme_name', models.CharField(max_length=200)),
                ('duration', models.IntegerField(max_length=2)),
                ('branch', models.ForeignKey(to='collection.dept')),
            ],
        ),
    ]
