# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'RemoteHost'
        db.delete_table(u'base_remotehost')

        # Removing M2M table for field r_hashes on 'Event'
        db.delete_table(db.shorten_name(u'base_event_r_hashes'))

        # Adding M2M table for field session_keys on 'Event'
        m2m_table_name = db.shorten_name(u'base_event_session_keys')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'base.event'], null=False)),
            ('session', models.ForeignKey(orm[u'sessions.session'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'session_id'])


    def backwards(self, orm):
        # Adding model 'RemoteHost'
        db.create_table(u'base_remotehost', (
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.TextField')()),
            ('last_access', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('r_hash', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True)),
        ))
        db.send_create_signal(u'base', ['RemoteHost'])

        # Adding M2M table for field r_hashes on 'Event'
        m2m_table_name = db.shorten_name(u'base_event_r_hashes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'base.event'], null=False)),
            ('remotehost', models.ForeignKey(orm[u'base.remotehost'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'remotehost_id'])

        # Removing M2M table for field session_keys on 'Event'
        db.delete_table(db.shorten_name(u'base_event_session_keys'))


    models = {
        u'base.event': {
            'Meta': {'ordering': "(u'event_datetime',)", 'object_name': 'Event'},
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
        },
        u'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['base']