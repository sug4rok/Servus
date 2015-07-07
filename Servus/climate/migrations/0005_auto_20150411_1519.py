# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate', '0004_auto_20150411_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temphumidvalue',
            old_name='sensor_datetime',
            new_name='datetime',
        ),
    ]
