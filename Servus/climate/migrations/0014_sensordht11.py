# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arduino_dht11', '0001_initial'),
        ('base', '0014_remove_application_location'),
        ('climate', '0013_auto_20150715_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorDHT11',
            fields=[
                ('is_used', models.BooleanField(default=False, verbose_name=b'\xd0\x97\xd0\xb0\xd0\xb4\xd0\xb5\xd0\xb9\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd')),
                ('parent', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, to='arduino_dht11.SensorDHT11')),
                ('location', models.ForeignKey(verbose_name=b'\xd0\xa0\xd0\xb0\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5', to='base.Location', help_text=b'\xd0\x9c\xd0\xb5\xd1\x81\xd1\x82\xd0\xbe \xd1\x80\xd0\xb0\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xbe\xd0\xb1\xd1\x8a\xd0\xb5\xd0\xba\xd1\x82\xd0\xb0 \xd0\xb2 \xd0\xbf\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb8')),
            ],
            bases=('arduino_dht11.sensordht11',),
        ),
    ]
