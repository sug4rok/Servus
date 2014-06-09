# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'base_event')

        # Removing M2M table for field session_keys on 'Event'
        db.delete_table(db.shorten_name(u'base_event_session_keys'))


    def backwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'base_event', (
            ('event_imp', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2, max_length=1)),
            ('event_descr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('event_src', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('was_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['Event'])

        # Adding M2M table for field session_keys on 'Event'
        m2m_table_name = db.shorten_name(u'base_event_session_keys')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'base.event'], null=False)),
            ('session', models.ForeignKey(orm[u'sessions.session'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'session_id'])


    models = {
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
            'app_name': ('django.db.models.fields.CharField', [], {'default': "'home'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shown': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sub_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tab_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['base']