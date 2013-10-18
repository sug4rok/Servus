# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Weather'
        db.create_table(u'weather_weather', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weather_provider', self.gf('django.db.models.fields.CharField')(default='rp5', max_length=3)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default='2013-08-30 00:00')),
            ('clouds', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('precipitation', self.gf('django.db.models.fields.FloatField')(default=0.0, max_length=4)),
            ('temperature', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3)),
            ('pressure', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3)),
            ('humidity', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('wind_speed', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('wind_direction', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3)),
            ('clouds_img', self.gf('django.db.models.fields.CharField')(default='na', max_length=3)),
            ('falls_img', self.gf('django.db.models.fields.CharField')(default='na', max_length=4)),
        ))
        db.send_create_signal(u'weather', ['Weather'])


    def backwards(self, orm):
        # Deleting model 'Weather'
        db.delete_table(u'weather_weather')


    models = {
        u'weather.weather': {
            'Meta': {'object_name': 'Weather'},
            'clouds': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'clouds_img': ('django.db.models.fields.CharField', [], {'default': "'na'", 'max_length': '3'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': "'2013-08-30 00:00'"}),
            'falls_img': ('django.db.models.fields.CharField', [], {'default': "'na'", 'max_length': '4'}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precipitation': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'max_length': '4'}),
            'pressure': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'temperature': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'weather_provider': ('django.db.models.fields.CharField', [], {'default': "'rp5'", 'max_length': '3'}),
            'wind_direction': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'wind_speed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'})
        }
    }

    complete_apps = ['weather']