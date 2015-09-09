# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('weather', '0008_auto_20150903_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('datetime', models.DateTimeField(default=b'2013-08-30 00:00', help_text=b'', verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xbf\xd1\x80\xd0\xbe\xd0\xb3\xd0\xbd\xd0\xbe\xd0\xb7\xd0\xb0')),
                ('clouds', models.PositiveSmallIntegerField(default=0, verbose_name=b'\xd0\x9e\xd0\xb1\xd0\xbb\xd0\xb0\xd1\x87\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c')),
                ('precipitation', models.FloatField(default=0.0, max_length=4, verbose_name=b'\xd0\x9e\xd1\x81\xd0\xb0\xd0\xb4\xd0\xba\xd0\xb8')),
                ('temperature', models.SmallIntegerField(default=0, help_text=b'\xc2\xb0C', verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbc\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd1\x83\xd1\x80\xd0\xb0')),
                ('pressure', models.PositiveSmallIntegerField(default=0, help_text=b'\xd0\xbc\xd0\xbc \xd1\x80\xd1\x82. \xd1\x81\xd1\x82.', verbose_name=b'\xd0\x94\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('humidity', models.PositiveSmallIntegerField(default=0, help_text=b'%', verbose_name=b'\xd0\x92\xd0\xbb\xd0\xb0\xd0\xb6\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c')),
                ('wind_speed', models.PositiveSmallIntegerField(default=0, help_text=b'\xd0\xbc/c', verbose_name=b'\xd0\x92\xd0\xb5\xd1\x82\xd0\xb5\xd1\x80')),
                ('wind_direction', models.SmallIntegerField(default=0, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb2\xd0\xb5\xd1\x82\xd1\x80\xd0\xb0')),
                ('clouds_img', models.CharField(default=b'na', max_length=3)),
                ('falls_img', models.CharField(default=b'na', max_length=4)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('content_type', 'datetime'),
            },
        ),
        migrations.RemoveField(
            model_name='weather',
            name='content_type',
        ),
        migrations.DeleteModel(
            name='Weather',
        ),
    ]
