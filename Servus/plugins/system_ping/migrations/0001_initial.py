# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PingHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'\xd0\x98\xd0\xbc\xd1\x8f/\xd0\xbd\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x85\xd0\xbe\xd1\x81\xd1\x82\xd0\xb0')),
                ('ip_address', models.GenericIPAddressField(default=b'0.0.0.0', protocol=b'IPv4', verbose_name=b'IP-\xd0\xb0\xd0\xb4\xd1\x80\xd0\xb5\xd1\x81')),
                ('online', models.BooleanField(default=False, editable=False)),
                ('last_changed', models.DateTimeField(auto_now_add=True, verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xbf\xd0\xbe\xd1\x81\xd0\xbb\xd0\xb5\xd0\xb4\xd0\xbd\xd0\xb5\xd0\xb9 \xd1\x81\xd0\xbc\xd0\xb5\xd0\xbd\xd1\x8b \xd1\x81\xd1\x82\xd0\xb0\xd1\x82\xd1\x83\xd1\x81\xd0\xb0')),
            ],
            options={
                'verbose_name': '\u0445\u043e\u0441\u0442',
                'verbose_name_plural': '\u0421\u0435\u0442\u0435\u0432\u044b\u0435 \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430',
            },
        ),
    ]
