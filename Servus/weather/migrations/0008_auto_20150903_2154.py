# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('weather', '0007_yandexru'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weather',
            options={'ordering': ('content_type', 'datetime')},
        ),
        migrations.RemoveField(
            model_name='weather',
            name='wp',
        ),
        migrations.AddField(
            model_name='weather',
            name='content_type',
            field=models.ForeignKey(default=29, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weather',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='yandexru',
            name='location',
            field=models.ForeignKey(verbose_name=b'\xd0\xa0\xd0\xb0\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5', to='base.Location', help_text=b'\xd0\x9c\xd0\xb5\xd1\x81\xd1\x82\xd0\xbe \xd1\x80\xd0\xb0\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xbe\xd0\xb1\xd1\x8a\xd0\xb5\xd0\xba\xd1\x82\xd0\xb0 \xd0\xb2 \xd0\xbf\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb8 \xd0\xb8\xd0\xbb\xd0\xb8 \xd0\xb2\xd0\xbd\xd0\xb5 \xd0\xb5\xd0\xb3\xd0\xbe'),
        ),
        migrations.DeleteModel(
            name='WeatherProvider',
        ),
    ]
