# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate', '0012_auto_20150702_1251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temphumidvalueshort',
            name='sensor',
        ),
        migrations.DeleteModel(
            name='TempHumidValueShort',
        ),
    ]
