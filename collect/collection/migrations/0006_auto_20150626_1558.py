# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_auto_20150626_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvedcourselist',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposedcourselist',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='approvedcourselist',
            name='course_code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='proposedcourselist',
            name='course_code',
            field=models.CharField(max_length=10),
        ),
    ]
