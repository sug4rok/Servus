# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventRule'
        db.create_table(u'base_eventrule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_src', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Tab'])),
            ('event_descr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('event_imp', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
        ))
        db.send_create_signal(u'base', ['EventRule'])


        # Renaming column for 'Event.event_src' to match new field type.
        db.rename_column(u'base_event', 'event_src_id', 'event_src')
        # Changing field 'Event.event_src'
        db.alter_column(u'base_event', 'event_src', self.gf('django.db.models.fields.CharField')(max_length=20))


    def backwards(self, orm):
        # Adding index on 'Event', fields ['event_src']
        db.create_index(u'base_event', ['event_src_id'])

        # Deleting model 'EventRule'
        db.delete_table(u'base_eventrule')


        # Renaming column for 'Event.event_src' to match new field type.
        db.rename_column(u'base_event', 'event_src', 'event_src_id')
        # Changing field 'Event.event_src'
        db.alter_column(u'base_event', 'event_src_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Tab']))

    models = {
        u'base.event': {
            'Meta': {'ordering': "(u'event_datetime',)", 'object_name': 'Event'},
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'event_imp': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'event_src': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r_hashes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['base.RemoteHost']", 'symmetrical': 'False'})
        },
        u'base.eventrule': {
            'Meta': {'object_name': 'EventRule'},
            'event_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'event_imp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'event_src': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.Tab']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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