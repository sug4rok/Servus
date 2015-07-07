# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20150528_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tab',
            name='app_name',
            field=models.SlugField(default=b'home', max_length=20, verbose_name=b'\xd0\xa2\xd0\xb8\xd0\xbf \xd0\xbf\xd1\x80\xd0\xb8\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f'),
        ),
        migrations.AlterField(
            model_name='tab',
            name='tab_name',
            field=models.SlugField(max_length=20, verbose_name=b'\xd0\x92\xd0\xba\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xba\xd0\xb0'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f'),
        ),
    ]
