# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arduino_dht11', '0002_auto_20150831_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordht11',
            name='controller_pin',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name=b'\xd0\x92\xd1\x8b\xd0\xb2\xd0\xbe\xd0\xb4 (pin) \xd0\xbd\xd0\xb0 Arduino'),
        ),
    ]
