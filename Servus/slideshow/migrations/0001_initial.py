# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slideshow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('album_path', models.CharField(unique=True, max_length=255, verbose_name=b'\xd0\xa4\xd0\xbe\xd1\x82\xd0\xbe\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xb1\xd0\xbe\xd0\xbc')),
                ('is_shown', models.BooleanField(default=True, help_text=b'\xd0\x9e\xd1\x82\xd0\xbe\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5/\xd0\x98\xd1\x81\xd0\xba\xd0\xbb\xd1\x8e\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x84\xd0\xbe\xd1\x82\xd0\xbe\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xb1\xd0\xbe\xd0\xbc\xd0\xb0 \xd0\xb8\xd0\xb7 \xd0\xbf\xd0\xbe\xd0\xba\xd0\xb0\xd0\xb7\xd0\xb0 \xd0\xbd\xd0\xb0 \xd0\x93\xd0\xbb\xd0\xb0\xd0\xb2\xd0\xbd\xd0\xbe\xd0\xb9 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb5', verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xba\xd0\xb0\xd0\xb7\xd1\x8b\xd0\xb2\xd0\xb0\xd1\x82\xd1\x8c')),
            ],
            options={
                'verbose_name': '\u0424\u043e\u0442\u043e\u0430\u043b\u044c\u0431\u043e\u043c',
                'verbose_name_plural': '\u0424\u043e\u0442\u043e\u0430\u043b\u044c\u0431\u043e\u043c\u044b \u0432 \u043f\u0430\u043f\u043a\u0435 slideshow',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SlideshowChanges',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mtime', models.FloatField(default=0.0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
