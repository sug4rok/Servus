# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_auto_20150529_1444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weatherprovider',
            old_name='weather_city',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='weatherprovider',
            old_name='weather_url',
            new_name='url',
        ),
    ]
