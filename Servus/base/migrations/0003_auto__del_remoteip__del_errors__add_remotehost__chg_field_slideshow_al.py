# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'RemoteIP'
        db.delete_table(u'base_remoteip')

        # Deleting model 'Errors'
        db.delete_table(u'base_errors')

        # Adding model 'RemoteHost'
        db.create_table(u'base_remotehost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.TextField')()),
            ('r_hash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('last_access', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['RemoteHost'])


        # Changing field 'Slideshow.album_path'
        db.alter_column(u'base_slideshow', 'album_path', self.gf('django.db.models.fields.FilePathField')(max_length=100))
        # Removing M2M table for field ips on 'Events'
        db.delete_table(db.shorten_name(u'base_events_ips'))

        # Adding M2M table for field r_hashes on 'Events'
        m2m_table_name = db.shorten_name(u'base_events_r_hashes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('events', models.ForeignKey(orm[u'base.events'], null=False)),
            ('remotehost', models.ForeignKey(orm[u'base.remotehost'], null=False))
        ))
        db.create_unique(m2m_table_name, ['events_id', 'remotehost_id'])


    def backwards(self, orm):
        # Adding model 'RemoteIP'
        db.create_table(u'base_remoteip', (
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('last_access', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'base', ['RemoteIP'])

        # Adding model 'Errors'
        db.create_table(u'base_errors', (
            ('error_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('error_viewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('error_descr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('error_src', self.gf('django.db.models.fields.CharField')(max_length=15)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'base', ['Errors'])

        # Deleting model 'RemoteHost'
        db.delete_table(u'base_remotehost')


        # Changing field 'Slideshow.album_path'
        db.alter_column(u'base_slideshow', 'album_path', self.gf('django.db.models.fields.files.ImageField')(max_length=100))
        # Adding M2M table for field ips on 'Events'
        m2m_table_name = db.shorten_name(u'base_events_ips')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('events', models.ForeignKey(orm[u'base.events'], null=False)),
            ('remoteip', models.ForeignKey(orm[u'base.remoteip'], null=False))
        ))
        db.create_unique(m2m_table_name, ['events_id', 'remoteip_id'])

        # Removing M2M table for field r_hashes on 'Events'
        db.delete_table(db.shorten_name(u'base_events_r_hashes'))


    models = {
        u'base.events': {
            'Meta': {'ordering': "('event_datetime',)", 'object_name': 'Events'},
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'event_imp': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'event_src': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'r_hashes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['base.RemoteHost']", 'symmetrical': 'False'})
        },
        u'base.mtime': {
            'Meta': {'object_name': 'MTime'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtime': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'base.remotehost': {
            'Meta': {'object_name': 'RemoteHost'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'r_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'user_agent': ('django.db.models.fields.TextField', [], {})
        },
        u'base.slideshow': {
            'Meta': {'object_name': 'Slideshow'},
            'album_path': ('django.db.models.fields.FilePathField', [], {'max_length': '100'}),
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