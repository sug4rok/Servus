# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tab'
        db.create_table(u'base_tab', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tab_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('sub_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['Tab'])

        # Adding model 'Events'
        db.create_table(u'base_events', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_src', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('event_descr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('event_imp', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('event_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event_viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'base', ['Events'])

        # Adding model 'Errors'
        db.create_table(u'base_errors', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('error_src', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('error_descr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('error_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('error_viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'base', ['Errors'])

        # Adding model 'RemoteIP'
        db.create_table(u'base_remoteip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('last_access', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['RemoteIP'])

        # Adding model 'MTime'
        db.create_table(u'base_mtime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mtime', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'base', ['MTime'])

        # Adding model 'Slideshow'
        db.create_table(u'base_slideshow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album_path', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'base', ['Slideshow'])


    def backwards(self, orm):
        # Deleting model 'Tab'
        db.delete_table(u'base_tab')

        # Deleting model 'Events'
        db.delete_table(u'base_events')

        # Deleting model 'Errors'
        db.delete_table(u'base_errors')

        # Deleting model 'RemoteIP'
        db.delete_table(u'base_remoteip')

        # Deleting model 'MTime'
        db.delete_table(u'base_mtime')

        # Deleting model 'Slideshow'
        db.delete_table(u'base_slideshow')


    models = {
        u'base.errors': {
            'Meta': {'object_name': 'Errors'},
            'error_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'error_src': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'error_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'base.events': {
            'Meta': {'object_name': 'Events'},
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'event_imp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'event_src': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'event_viewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'base.mtime': {
            'Meta': {'object_name': 'MTime'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtime': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'base.remoteip': {
            'Meta': {'object_name': 'RemoteIP'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'base.slideshow': {
            'Meta': {'object_name': 'Slideshow'},
            'album_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
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