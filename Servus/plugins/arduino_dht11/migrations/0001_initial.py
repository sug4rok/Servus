# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arduino', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorDHT11',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(unique=True, max_length=10, verbose_name=b'\xd0\xa1\xd0\xb8\xd1\x81\xd1\x82\xd0\xb5\xd0\xbc\xd0\xbd\xd0\xbe\xd0\xb5 \xd0\xb8\xd0\xbc\xd1\x8f')),
                ('controller_pin', models.PositiveSmallIntegerField(unique=True, verbose_name=b'\xd0\x92\xd1\x8b\xd0\xb2\xd0\xbe\xd0\xb4 (pin) \xd0\xbd\xd0\xb0 Arduino')),
                ('location_type', models.SlugField(default=b'inside', verbose_name=b'\xd0\xa2\xd0\xb8\xd0\xbf \xd1\x80\xd0\xb0\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb4\xd0\xb0\xd1\x82\xd1\x87\xd0\xb8\xd0\xba\xd0\xb0', choices=[(b'inside', b'\xd0\x92 \xd0\xbf\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb8'), (b'outside', b'\xd0\x9d\xd0\xb0 \xd1\x83\xd0\xbb\xd0\xb8\xd1\x86\xd0\xb5'), (b'other', b'\xd0\x94\xd1\x80\xd1\x83\xd0\xb3\xd0\xbe\xd0\xb5')])),
                ('controller', models.ForeignKey(verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xbd\xd1\x82\xd1\x80\xd0\xbe\xd0\xbb\xd0\xbb\xd0\xb5\xd1\x80 Arduino', to='arduino.Arduino')),
            ],
            options={
                'verbose_name': '\u0414\u0430\u0442\u0447\u0438\u043a DHT11',
                'verbose_name_plural': '\u0414\u0430\u0442\u0447\u0438\u043a\u0438 DHT11',
            },
        ),
    ]
