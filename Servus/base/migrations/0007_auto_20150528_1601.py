# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20150528_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tab',
            options={'ordering': ('id',), 'verbose_name': '\u0412\u043a\u043b\u0430\u0434\u043a\u0443', 'verbose_name_plural': '\u0412\u043a\u043b\u0430\u0434\u043a\u0438'},
        ),
    ]
