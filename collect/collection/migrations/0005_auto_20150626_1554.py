# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0004_programme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvedcourselist',
            name='dept',
        ),
        migrations.RemoveField(
            model_name='approvedcourseteaching',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='foreigncourselist',
            name='dept',
        ),
        migrations.RemoveField(
            model_name='proposedcourseteaching',
            name='branch',
        ),
        migrations.AddField(
            model_name='approvedcourselist',
            name='programme',
            field=models.ForeignKey(default=1, to='collection.programme'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='approvedcourseteaching',
            name='programme',
            field=models.ForeignKey(default=1, to='collection.programme'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='foreigncourselist',
            name='programme',
            field=models.ForeignKey(default=1, to='collection.programme'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposedcourselist',
            name='programme',
            field=models.ForeignKey(default=1, to='collection.programme'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposedcourseteaching',
            name='programme',
            field=models.ForeignKey(default=1, to='collection.programme'),
            preserve_default=False,
        ),
    ]
