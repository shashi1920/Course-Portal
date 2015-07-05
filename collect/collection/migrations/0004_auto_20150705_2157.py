# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_remove_approvedcourseteaching_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log', models.CharField(max_length=1500)),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('USER', models.ForeignKey(to='collection.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='approvedcourselist',
            name='l',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='approvedcourselist',
            name='p',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='approvedcourselist',
            name='t',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
