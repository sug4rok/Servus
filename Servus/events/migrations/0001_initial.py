# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'events_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_src', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('event_descr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('event_imp', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2, max_length=1)),
            ('event_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('was_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'events', ['Event'])

        # Adding M2M table for field session_keys on 'Event'
        m2m_table_name = db.shorten_name(u'events_event_session_keys')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'events.event'], null=False)),
            ('session', models.ForeignKey(orm[u'sessions.session'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'session_id'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'events_event')

        # Removing M2M table for field session_keys on 'Event'
        db.delete_table(db.shorten_name(u'events_event_session_keys'))


    models = {
        u'events.event': {
            'Meta': {'ordering': "('event_datetime',)", 'object_name': 'Event'},
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'event_imp': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2', 'max_length': '1'}),
            'event_src': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_keys': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sessions.Session']", 'symmetrical': 'False'}),
            'was_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['events']