# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SlideshowExclude'
        db.delete_table(u'base_slideshowexclude')

        # Adding field 'Slideshow.is_shown'
        db.add_column(u'base_slideshow', 'is_shown',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


        # Changing field 'Slideshow.album_path'
        db.alter_column(u'base_slideshow', 'album_path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))
        # Adding unique constraint on 'Slideshow', fields ['album_path']
        db.create_unique(u'base_slideshow', ['album_path'])

        # Deleting field 'SlideshowChanges.was_excluded'
        db.delete_column(u'base_slideshowchanges', 'was_excluded')


    def backwards(self, orm):
        # Removing unique constraint on 'Slideshow', fields ['album_path']
        db.delete_unique(u'base_slideshow', ['album_path'])

        # Adding model 'SlideshowExclude'
        db.create_table(u'base_slideshowexclude', (
            ('album_exclude', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'base', ['SlideshowExclude'])

        # Deleting field 'Slideshow.is_shown'
        db.delete_column(u'base_slideshow', 'is_shown')


        # Changing field 'Slideshow.album_path'
        db.alter_column(u'base_slideshow', 'album_path', self.gf('django.db.models.fields.files.ImageField')(max_length=100))
        # Adding field 'SlideshowChanges.was_excluded'
        db.add_column(u'base_slideshowchanges', 'was_excluded',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'base.event': {
            'Meta': {'ordering': "('event_datetime',)", 'object_name': 'Event'},
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'event_imp': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'event_src': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_keys': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sessions.Session']", 'symmetrical': 'False'})
        },
        u'base.eventrule': {
            'Meta': {'object_name': 'EventRule'},
            'event_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'event_imp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'event_src': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Tab']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'base.slideshow': {
            'Meta': {'object_name': 'Slideshow'},
            'album_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shown': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'base.slideshowchanges': {
            'Meta': {'object_name': 'SlideshowChanges'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtime': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'base.tab': {
            'Meta': {'object_name': 'Tab'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tab_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['base']