# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate', '0003_auto_20150411_1454'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temphumidvalue',
            old_name='sensor_name',
            new_name='sensor',
        ),
        migrations.RenameField(
            model_name='temphumidvalueshort',
            old_name='sensor_name',
            new_name='sensor',
        ),
    ]
