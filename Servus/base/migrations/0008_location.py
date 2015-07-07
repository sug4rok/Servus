# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20150528_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(help_text=b'\xd0\x9c\xd0\xb5\xd1\x81\xd1\x82\xd0\xbe, \xd0\xb3\xd0\xb4\xd0\xb5 \xd1\x80\xd0\xb0\xd0\xb7\xd0\xbc\xd0\xb5\xd1\x89\xd0\xb0\xd0\xb5\xd1\x82\xd1\x81\xd1\x8f \xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd1\x80\xd0\xbe\xd0\xbb\xd0\xb8\xd1\x80\xd1\x83\xd0\xb5\xd0\xbc\xd1\x8b\xd0\xb9 \xd0\xbe\xd0\xb1\xd1\x8a\xd0\xb5\xd0\xba\xd1\x82', max_length=20, verbose_name=b'\xd0\xa0\xd0\xb0\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('description', models.CharField(max_length=50, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xbc\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb0\xd1\x80\xd0\xb8\xd0\xb9', blank=True)),
            ],
            options={
                'verbose_name': '\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f',
            },
        ),
    ]
