# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate', '0002_auto_20150411_1347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temphumidsensor',
            old_name='sensor_pin',
            new_name='arduino_pin',
        ),
        migrations.RenameField(
            model_name='temphumidsensor',
            old_name='sensor_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='temphumidsensor',
            old_name='sensor_verb_name',
            new_name='verbose_name',
        ),
    ]
