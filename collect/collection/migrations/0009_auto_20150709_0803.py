# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0008_auto_20150709_0745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foreigncourselist',
            name='level_0',
        ),
        migrations.RemoveField(
            model_name='foreigncourselist',
            name='level_1',
        ),
        migrations.RemoveField(
            model_name='foreigncourselist',
            name='level_2',
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 9, 2, 33, 21, 442000, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='prof_id1',
            field=models.ForeignKey(blank=True, to='collection.Professor', null=True),
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='prof_id2',
            field=models.ForeignKey(related_name='fr_prof_id2', blank=True, to='collection.Professor', null=True),
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='prof_id3',
            field=models.ForeignKey(related_name='fr_prof_id3', blank=True, to='collection.Professor', null=True),
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='prof_id4',
            field=models.ForeignKey(related_name='fr_prof_id4', blank=True, to='collection.Professor', null=True),
        ),
    ]
