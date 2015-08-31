# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('climate', '0014_sensordht11'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temphumidsensor',
            name='location',
        ),
        migrations.RemoveField(
            model_name='temphumidvalue',
            name='sensor',
        ),
        migrations.AddField(
            model_name='temphumidvalue',
            name='content_type',
            field=models.ForeignKey(default=25, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temphumidvalue',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TempHumidSensor',
        ),
    ]
