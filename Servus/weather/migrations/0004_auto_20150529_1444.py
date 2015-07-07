# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_auto_20150411_1347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weatherprovider',
            old_name='weather_provider',
            new_name='name',
        ),
    ]
