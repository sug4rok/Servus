# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Slideshow'
        db.delete_table(u'base_slideshow')

        # Deleting model 'SlideshowChanges'
        db.delete_table(u'base_slideshowchanges')


    def backwards(self, orm):
        # Adding model 'Slideshow'
        db.create_table(u'base_slideshow', (
            ('is_shown', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album_path', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal(u'base', ['Slideshow'])

        # Adding model 'SlideshowChanges'
        db.create_table(u'base_slideshowchanges', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mtime', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'base', ['SlideshowChanges'])


    models = {
        u'base.tab': {
            'Meta': {'object_name': 'Tab'},
            'app_name': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shown': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tab_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'base.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'phone': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'sms_ru_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['base']