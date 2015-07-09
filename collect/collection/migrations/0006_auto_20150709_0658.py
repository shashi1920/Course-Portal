# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_auto_20150708_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvedcourseteaching',
            name='fr_course_code',
            field=models.ForeignKey(blank=True, to='collection.ForeignCourseList', null=True),
        ),
        migrations.AlterField(
            model_name='approvedcourseteaching',
            name='course_code',
            field=models.ForeignKey(blank=True, to='collection.ApprovedCourseList', null=True),
        ),
    ]
