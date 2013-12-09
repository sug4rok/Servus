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

        # Adding model 'RemoteHost'
        db.create_table(u'base_remotehost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(default='127.0.0.1', max_length=15)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.TextField')()),
            ('r_hash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('last_access', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['RemoteHost'])

        # Adding model 'Event'
        db.create_table(u'base_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_src', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Tab'])),
            ('event_descr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('event_imp', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('event_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['Event'])

        # Adding M2M table for field r_hashes on 'Event'
        m2m_table_name = db.shorten_name(u'base_event_r_hashes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'base.event'], null=False)),
            ('remotehost', models.ForeignKey(orm[u'base.remotehost'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'remotehost_id'])

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
        u'base.mtime': {
            'Meta': {'object_name': 'MTime'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtime': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
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


def backwards(orm):
    # Deleting model 'Tab'
    db.delete_table(u'base_tab')

    # Deleting model 'RemoteHost'
    db.delete_table(u'base_remotehost')

    # Deleting model 'Event'
    db.delete_table(u'base_event')

    # Removing M2M table for field r_hashes on 'Event'
    db.delete_table(db.shorten_name(u'base_event_r_hashes'))

    # Deleting model 'MTime'
    db.delete_table(u'base_mtime')

    # Deleting model 'Slideshow'
    db.delete_table(u'base_slideshow')