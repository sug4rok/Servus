# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_src', models.CharField(max_length=20, verbose_name=b'\xd0\x98\xd1\x81\xd1\x82\xd0\xbe\xd1\x87\xd0\xbd\xd0\xb8\xd0\xba \xd1\x81\xd0\xbe\xd0\xb1\xd1\x8b\xd1\x82\xd0\xb8\xd1\x8f')),
                ('event_descr', models.CharField(max_length=255, null=True, verbose_name=b'\xd0\x9e\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x81\xd0\xbe\xd0\xb1\xd1\x8b\xd1\x82\xd0\xb8\xd1\x8f')),
                ('event_imp', models.PositiveSmallIntegerField(default=2, max_length=1, verbose_name=b'\xd0\x9a\xd1\x80\xd0\xb8\xd1\x82\xd0\xb8\xd1\x87\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c')),
                ('event_datetime', models.DateTimeField(auto_now_add=True, verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xb2\xd0\xbe\xd0\xb7\xd0\xbd\xd0\xb8\xd0\xba\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x81\xd0\xbe\xd0\xb1\xd1\x8b\xd1\x82\xd0\xb8\xd1\x8f')),
                ('email_sent', models.BooleanField(default=False)),
                ('sms_sent', models.BooleanField(default=False)),
                ('session_keys', models.ManyToManyField(to='sessions.Session', editable=False)),
            ],
            options={
                'ordering': ('event_datetime',),
            },
            bases=(models.Model,),
        ),
    ]
