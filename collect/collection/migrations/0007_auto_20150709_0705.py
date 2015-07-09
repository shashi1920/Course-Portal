# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0006_auto_20150709_0658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvedcourseteaching',
            name='fr_course_code',
        ),
        migrations.AlterField(
            model_name='approvedcourseteaching',
            name='course_code',
            field=models.ForeignKey(default=1, to='collection.ApprovedCourseList'),
            preserve_default=False,
        ),
    ]
