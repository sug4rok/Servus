# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Plan'
        db.create_table(u'home_plan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('plan_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('plan_file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('is_shown', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'home', ['Plan'])


    def backwards(self, orm):
        # Deleting model 'Plan'
        db.delete_table(u'home_plan')


    models = {
        u'home.plan': {
            'Meta': {'object_name': 'Plan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shown': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'plan_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'plan_name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['home']