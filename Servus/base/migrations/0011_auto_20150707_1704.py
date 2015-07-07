# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20150704_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tab',
            name='tab_name',
            field=models.CharField(max_length=20, verbose_name=b'\xd0\x92\xd0\xba\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xba\xd0\xb0'),
        ),
    ]
