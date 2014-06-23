# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.was_sent'
        db.delete_column(u'events_event', 'was_sent')

        # Adding field 'Event.email_sent'
        db.add_column(u'events_event', 'email_sent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Event.sms_sent'
        db.add_column(u'events_event', 'sms_sent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Event.was_sent'
        db.add_column(u'events_event', 'was_sent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Event.email_sent'
        db.delete_column(u'events_event', 'email_sent')

        # Deleting field 'Event.sms_sent'
        db.delete_column(u'events_event', 'sms_sent')


    models = {
        u'events.event': {
            'Meta': {'ordering': "('event_datetime',)", 'object_name': 'Event'},
            'email_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event_descr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'event_imp': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2', 'max_length': '1'}),
            'event_src': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_keys': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sessions.Session']", 'symmetrical': 'False'}),
            'sms_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['events']