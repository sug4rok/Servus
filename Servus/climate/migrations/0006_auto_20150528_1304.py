# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('climate', '0005_auto_20150411_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='temphumidsensor',
            name='location',
            field=models.SlugField(default=b'inside', verbose_name=b'\xd0\xa0\xd0\xb0\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb4\xd0\xb0\xd1\x82\xd1\x87\xd0\xb8\xd0\xba\xd0\xb0', choices=[(b'inside', b'\xd0\x92 \xd0\xbf\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb8'), (b'outside', b'\xd0\x9d\xd0\xb0 \xd1\x83\xd0\xbb\xd0\xb8\xd1\x86\xd0\xb5'), (b'other', b'\xd0\x94\xd1\x80\xd1\x83\xd0\xb3\xd0\xbe\xd0\xb5')]),
        ),
        migrations.AlterField(
            model_name='temphumidsensor',
            name='name',
            field=models.SlugField(unique=True, max_length=10, verbose_name=b'\xd0\xa1\xd0\xb8\xd1\x81\xd1\x82\xd0\xb5\xd0\xbc\xd0\xbd\xd0\xbe\xd0\xb5 \xd0\xb8\xd0\xbc\xd1\x8f'),
        ),
    ]
