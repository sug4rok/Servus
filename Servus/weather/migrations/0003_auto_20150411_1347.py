# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_weatherprovider_is_used'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weather',
            options={'ordering': ('wp', 'datetime')},
        ),
        migrations.AlterField(
            model_name='weather',
            name='clouds',
            field=models.PositiveSmallIntegerField(default=0, verbose_name=b'\xd0\x9e\xd0\xb1\xd0\xbb\xd0\xb0\xd1\x87\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='datetime',
            field=models.DateTimeField(default=b'2013-08-30 00:00', help_text=b'', verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xbf\xd1\x80\xd0\xbe\xd0\xb3\xd0\xbd\xd0\xbe\xd0\xb7\xd0\xb0'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='humidity',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'%', verbose_name=b'\xd0\x92\xd0\xbb\xd0\xb0\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='pressure',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'\xd0\xbc\xd0\xbc \xd1\x80\xd1\x82. \xd1\x81\xd1\x82.', verbose_name=b'\xd0\x94\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='temperature',
            field=models.SmallIntegerField(default=0, help_text=b'\xc2\xb0C', verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbc\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd1\x83\xd1\x80\xd0\xb0'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='wind_direction',
            field=models.SmallIntegerField(default=0, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb2\xd0\xb5\xd1\x82\xd1\x80\xd0\xb0'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='wind_speed',
            field=models.PositiveSmallIntegerField(default=0, help_text=b'\xd0\xbc/c', verbose_name=b'\xd0\x92\xd0\xb5\xd1\x82\xd0\xb5\xd1\x80'),
        ),
    ]
