# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temphumidsensor',
            name='sensor_pin',
            field=models.PositiveSmallIntegerField(help_text=b'\xd0\x94\xd0\xbb\xd1\x8f \xd0\xb4\xd0\xb0\xd1\x82\xd1\x87\xd0\xb8\xd0\xba\xd0\xbe\xd0\xb2 \xd1\x82\xd0\xb5\xd0\xbc\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd1\x83\xd1\x80\xd1\x8b \xd0\xb2\xd1\x8b\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xbd\xd1\x8b \xd0\xb2\xd1\x8b\xd0\xb2\xd0\xbe\xd0\xb4\xd1\x8b \xd1\x81 2 \xd0\xbf\xd0\xbe 5', unique=True, verbose_name=b'\xd0\x92\xd1\x8b\xd0\xb2\xd0\xbe\xd0\xb4 (pin) \xd0\xbd\xd0\xb0 Arduino'),
        ),
        migrations.AlterField(
            model_name='temphumidvalue',
            name='humidity',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'\xd0\x92\xd0\xbb\xd0\xb0\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c'),
        ),
        migrations.AlterField(
            model_name='temphumidvalue',
            name='temperature',
            field=models.SmallIntegerField(default=0, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbc\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd1\x83\xd1\x80\xd0\xb0'),
        ),
        migrations.AlterField(
            model_name='temphumidvalueshort',
            name='humidity',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'\xd0\x92\xd0\xbb\xd0\xb0\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c'),
        ),
        migrations.AlterField(
            model_name='temphumidvalueshort',
            name='temperature',
            field=models.SmallIntegerField(default=0, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbc\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd1\x83\xd1\x80\xd0\xb0'),
        ),
    ]
