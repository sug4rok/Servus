# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150411_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('datetime',)},
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_datetime',
            new_name='datetime',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_imp',
            new_name='level',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_descr',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_src',
        ),
        migrations.AddField(
            model_name='event',
            name='message',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xd0\xa1\xd0\xbe\xd0\xbe\xd0\xb1\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5'),
        ),
        migrations.AddField(
            model_name='event',
            name='source',
            field=models.SlugField(default='system', max_length=20, verbose_name=b'\xd0\x98\xd1\x81\xd1\x82\xd0\xbe\xd1\x87\xd0\xbd\xd0\xb8\xd0\xba \xd1\x81\xd0\xbe\xd0\xb1\xd1\x8b\xd1\x82\xd0\xb8\xd1\x8f'),
            preserve_default=False,
        ),
    ]
