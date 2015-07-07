# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_imp',
            field=models.PositiveSmallIntegerField(default=2, verbose_name=b'\xd0\x9a\xd1\x80\xd0\xb8\xd1\x82\xd0\xb8\xd1\x87\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c'),
        ),
    ]
