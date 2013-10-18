# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Events.event_viewed'
        db.delete_column(u'base_events', 'event_viewed')

        # Adding M2M table for field ips on 'Events'
        m2m_table_name = db.shorten_name(u'base_events_ips')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('events', models.ForeignKey(orm[u'base.events'], null=False)),
            ('remoteip', models.ForeignKey(orm[u'base.remoteip'], null=False))
        ))
        db.create_unique(m2m_table_name, ['events_id', 'remoteip_id'])


    def backwards(self, orm):
        # Adding field 'Events.event_viewed'
        db.add_column(u'base_events', 'event_viewed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Removing M2M table for field ips on 'Events'
        db.delete_table(db.shorten_name(u'base_events_ips'))


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ips': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['base.RemoteIP']", 'symmetrical': 'False'})
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