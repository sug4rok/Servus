# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSRu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.BigIntegerField(help_text=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd0\xb0 \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xbe\xd1\x82\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xba\xd0\xb8 \xd1\x81\xd0\xbe\xd0\xbe\xd0\xb1\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb9 \xd1\x87\xd0\xb5\xd1\x80\xd0\xb5\xd0\xb7 \xd1\x81\xd0\xb5\xd1\x80\xd0\xb2\xd0\xb8\xd1\x81 sms.ru.<br>            \xd0\x94\xd0\xb8\xd0\xb0\xd0\xbf\xd0\xb0\xd0\xb7\xd0\xbe\xd0\xbd \xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80\xd0\xbe\xd0\xb2 \xd0\xbe\xd0\xb3\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x87\xd0\xb5\xd0\xbd 1*e10 - 9,(9)*e12 (\xd0\xbf\xd0\xbe\xd0\xb4\xd1\x80\xd0\xbe\xd0\xb1\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd0\xb8 \xd0\xbd\xd0\xb0 sms.ru).<br>            \xd0\xa4\xd0\xbe\xd1\x80\xd0\xbc\xd0\xb0\xd1\x82 \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xa0\xd0\xa4 7xxxyyyyyyy, \xd0\xb3\xd0\xb4\xd0\xb5 xxx - \xd0\xba\xd0\xbe\xd0\xb4 \xd0\xbe\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80\xd0\xb0, yyyyyyy - \xd0\xbd\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd0\xb0.<br>', verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd0\xb0', validators=[django.core.validators.MaxValueValidator(9999999999999L), django.core.validators.MinValueValidator(10000000000L)])),
                ('sms_ru_id', models.CharField(max_length=40, null=True, verbose_name=b'sms.ru api_id', blank=True)),
                ('name', models.ForeignKey(verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'sms.ru id',
                'verbose_name_plural': 'sms.ru id',
            },
        ),
    ]
