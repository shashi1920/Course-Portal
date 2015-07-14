# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0012_auto_20150709_0816'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('semester', models.IntegerField()),
                ('course', models.BooleanField(default=False)),
                ('minimum_elective', models.IntegerField()),
                ('allot', models.BooleanField(default=False)),
                ('programme', models.ForeignKey(to='collection.programme')),
            ],
        ),
    ]
