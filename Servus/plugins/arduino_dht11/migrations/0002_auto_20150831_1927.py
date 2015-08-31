# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arduino_dht11', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sensordht11',
            old_name='arduino',
            new_name='controller',
        ),
        migrations.RenameField(
            model_name='sensordht11',
            old_name='arduino_pin',
            new_name='controller_pin',
        ),
    ]
