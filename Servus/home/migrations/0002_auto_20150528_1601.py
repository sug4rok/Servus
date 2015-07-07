# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='plan_file',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='plan',
            old_name='plan_name',
            new_name='name',
        ),
    ]
