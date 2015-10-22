# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arduino',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'\xd0\x9c\xd0\xbe\xd0\xb4\xd0\xb5\xd0\xbb\xd1\x8c')),
                ('port', models.CharField(default=1, help_text=b'COM-\xd0\xbf\xd0\xbe\xd1\x80\xd1\x82, \xd0\xba \xd0\xba\xd0\xbe\xd1\x82\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbc\xd1\x83 \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd \xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd1\x80\xd0\xbe\xd0\xbb\xd0\xbb\xd0\xb5\xd1\x80.<br>                  \xd0\x9d\xd0\xb0\xd0\xbf\xd1\x80\xd0\xb8\xd0\xbc\xd0\xb5\xd1\x80:<br>                  \xd0\x92 Windows \xd0\xbf\xd0\xbe\xd1\x80\xd1\x82 = \xe2\x84\x96 \xd0\xbf\xd0\xbe\xd1\x80\xd1\x82\xd0\xb0 - 1;<br>                  \xd0\x92 Linux   \xd0\xbf\xd0\xbe\xd1\x80\xd1\x82 = /dev/ttyACM0', max_length=20, verbose_name=b'COM-\xd0\xbf\xd0\xbe\xd1\x80\xd1\x82')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0442\u0440\u043e\u043b\u043b\u0435\u0440 Arduino',
                'verbose_name_plural': '\u041a\u043e\u043d\u0442\u0440\u043e\u043b\u043b\u0435\u0440\u044b Arduino',
            },
        ),
    ]
