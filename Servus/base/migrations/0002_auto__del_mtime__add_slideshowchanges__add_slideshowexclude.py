# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MTime'
        db.delete_table(u'base_mtime')

        # Adding model 'SlideshowChanges'
        db.create_table(u'base_slideshowchanges', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mtime', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('was_excluded', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'base', ['SlideshowChanges'])

        # Adding model 'SlideshowExclude'
        db.create_table(u'base_slideshowexclude', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album_exclude', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'base', ['SlideshowExclude'])


    def backwards(self, orm):
        # Adding model 'MTime'
        db.create_table(u'base_mtime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mtime', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'base', ['MTime'])

        # Deleting model 'SlideshowChanges'
        db.delete_table(u'base_slideshowchanges')

        # Deleting model 'SlideshowExclude'
        db.delete_table(u'base_slideshowexclude')


    models = {
        u'base.event': {
            'Meta': {'ordering': "('event_datetime',)", 'object_name': 'Event'},
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'event_imp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'event_src': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Tab']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r_hashes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['base.RemoteHost']", 'symmetrical': 'False'})
        },
        u'base.remotehost': {
            'Meta': {'object_name': 'RemoteHost'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': "'127.0.0.1'", 'max_length': '15'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'r_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user_agent': ('django.db.models.fields.TextField', [], {})
        },
        u'base.slideshow': {
            'Meta': {'object_name': 'Slideshow'},
            'album_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'base.slideshowchanges': {
            'Meta': {'object_name': 'SlideshowChanges'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtime': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'was_excluded': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'base.slideshowexclude': {
            'Meta': {'object_name': 'SlideshowExclude'},
            'album_exclude': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'base.tab': {
            'Meta': {'object_name': 'Tab'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sub_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tab_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['base']