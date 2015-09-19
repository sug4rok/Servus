# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(unique=True, verbose_name=b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('is_tab', models.BooleanField(default=False, help_text=b'\xd0\x98\xd0\xbc\xd0\xb5\xd0\xb5\xd1\x82 \xd1\x81\xd0\xbe\xd0\xb1\xd1\x81\xd1\x82\xd0\xb2\xd0\xb5\xd0\xbd\xd0\xbd\xd1\x83\xd1\x8e \xd0\xb2\xd0\xba\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xba\xd1\x83 \xd0\xb2 \xd0\xbc\xd0\xb5\xd0\xbd\xd1\x8e web-\xd0\xb8\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd1\x84\xd0\xb5\xd0\xb9\xd1\x81\xd0\xb0', verbose_name=b'\xd0\x92\xd0\xba\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xba\xd0\xb0')),
                ('tab_name', models.CharField(max_length=20, verbose_name=b'\xd0\x92\xd0\xba\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xba\xd0\xb0')),
                ('title', models.CharField(max_length=50, null=True, verbose_name=b'\xd0\x97\xd0\xb0\xd0\xb3\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xba', blank=True)),
                ('sub_title', models.CharField(max_length=100, null=True, verbose_name=b'\xd0\x9a\xd1\x80\xd0\xb0\xd1\x82\xd0\xba\xd0\xbe\xd0\xb5 \xd0\xbe\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', blank=True)),
                ('is_widget', models.BooleanField(default=False, help_text=b'\xd0\x98\xd0\xbc\xd0\xb5\xd0\xb5\xd1\x82 \xd1\x81\xd0\xbe\xd0\xb1\xd1\x81\xd1\x82\xd0\xb2\xd0\xb5\xd0\xbd\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xb2\xd0\xb8\xd0\xb4\xd0\xb6\xd0\xb5\xd1\x82 \xd0\xbd\xd0\xb0 \xd0\x93\xd0\xbb\xd0\xb0\xd0\xb2\xd0\xbd\xd0\xbe\xd0\xb9 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb5', verbose_name=b'\xd0\x92\xd0\xb8\xd0\xb4\xd0\xb6\xd0\xb5\xd1\x82')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': '\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=20, blank=True, help_text=b'\xd0\x9c\xd0\xb5\xd1\x81\xd1\x82\xd0\xbe, \xd0\xb3\xd0\xb4\xd0\xb5 \xd1\x80\xd0\xb0\xd0\xb7\xd0\xbc\xd0\xb5\xd1\x89\xd0\xb0\xd0\xb5\xd1\x82\xd1\x81\xd1\x8f \xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd1\x80\xd0\xbe\xd0\xbb\xd0\xb8\xd1\x80\xd1\x83\xd0\xb5\xd0\xbc\xd1\x8b\xd0\xb9 \xd0\xbe\xd0\xb1\xd1\x8a\xd0\xb5\xd0\xba\xd1\x82', unique=True, verbose_name=b'\xd0\xa0\xd0\xb0\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('description', models.CharField(max_length=50, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xbc\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb0\xd1\x80\xd0\xb8\xd0\xb9', blank=True)),
            ],
            options={
                'verbose_name': '\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name=b'E-mail', blank=True)),
                ('phone', models.BigIntegerField(blank=True, help_text=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd0\xb0 \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xbe\xd1\x82\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xba\xd0\xb8 \xd1\x81\xd0\xbe\xd0\xbe\xd0\xb1\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb9 \xd1\x87\xd0\xb5\xd1\x80\xd0\xb5\xd0\xb7 \xd1\x81\xd0\xb5\xd1\x80\xd0\xb2\xd0\xb8\xd1\x81 sms.ru.<br>            \xd0\x94\xd0\xb8\xd0\xb0\xd0\xbf\xd0\xb0\xd0\xb7\xd0\xbe\xd0\xbd \xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80\xd0\xbe\xd0\xb2 \xd0\xbe\xd0\xb3\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x87\xd0\xb5\xd0\xbd 1*e10 - 9,(9)*e12 (\xd0\xbf\xd0\xbe\xd0\xb4\xd1\x80\xd0\xbe\xd0\xb1\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd0\xb8 \xd0\xbd\xd0\xb0 sms.ru).<br>            \xd0\xa4\xd0\xbe\xd1\x80\xd0\xbc\xd0\xb0\xd1\x82 \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xa0\xd0\xa4 7xxxyyyyyyy, \xd0\xb3\xd0\xb4\xd0\xb5 xxx - \xd0\xba\xd0\xbe\xd0\xb4 \xd0\xbe\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80\xd0\xb0, yyyyyyy - \xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd0\xb0.<br>', null=True, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd0\xb0', validators=[django.core.validators.MaxValueValidator(9999999999999L), django.core.validators.MinValueValidator(10000000000L)])),
                ('sms_ru_id', models.CharField(max_length=40, null=True, verbose_name=b'sms.ru api_id', blank=True)),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f',
                'verbose_name_plural': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438',
            },
        ),
    ]
