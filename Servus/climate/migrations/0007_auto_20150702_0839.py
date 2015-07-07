# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate', '0006_auto_20150528_1304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='temphumidsensor',
            old_name='location',
            new_name='location_type',
        ),
    ]
