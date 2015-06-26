# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foreigncourselist',
            name='dept',
            field=models.ForeignKey(default=1, to='collection.dept'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='foreigncourselist',
            name='course_code',
            field=models.CharField(max_length=10),
        ),
    ]
