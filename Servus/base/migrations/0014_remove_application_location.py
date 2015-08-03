# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20150714_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='location',
        ),
    ]
