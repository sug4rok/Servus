# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TempHumidSensor'
        db.create_table(u'climate_temphumidsensor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('sensor_verb_name', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('is_used', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'climate', ['TempHumidSensor'])

        # Adding model 'TempHumidValue'
        db.create_table(u'climate_temphumidvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['climate.TempHumidSensor'])),
            ('temperature', self.gf('django.db.models.fields.SmallIntegerField')(default=0, max_length=3)),
            ('humidity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, max_length=2)),
        ))
        db.send_create_signal(u'climate', ['TempHumidValue'])


    def backwards(self, orm):
        # Deleting model 'TempHumidSensor'
        db.delete_table(u'climate_temphumidsensor')

        # Deleting model 'TempHumidValue'
        db.delete_table(u'climate_temphumidvalue')


    models = {
        u'climate.temphumidsensor': {
            'Meta': {'object_name': 'TempHumidSensor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sensor_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'sensor_verb_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'climate.temphumidvalue': {
            'Meta': {'object_name': 'TempHumidValue'},
            'humidity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensor_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['climate.TempHumidSensor']"}),
            'temperature': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'max_length': '3'})
        }
    }

    complete_apps = ['climate']