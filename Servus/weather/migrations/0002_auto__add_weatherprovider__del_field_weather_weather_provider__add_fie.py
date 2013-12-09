# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WeatherProvider'
        db.create_table(u'weather_weatherprovider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weather_provider', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('weather_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('weather_city', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('on_sidebar', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'weather', ['WeatherProvider'])

        # Deleting field 'Weather.weather_provider'
        db.delete_column(u'weather_weather', 'weather_provider')

        # Adding field 'Weather.wp'
        db.add_column(u'weather_weather', 'wp',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['weather.WeatherProvider']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'WeatherProvider'
        db.delete_table(u'weather_weatherprovider')

        # Adding field 'Weather.weather_provider'
        db.add_column(u'weather_weather', 'weather_provider',
                      self.gf('django.db.models.fields.CharField')(default='rp5', max_length=3),
                      keep_default=False)

        # Deleting field 'Weather.wp'
        db.delete_column(u'weather_weather', 'wp_id')


    models = {
        u'weather.weather': {
            'Meta': {'ordering': "('wp',)", 'object_name': 'Weather'},
            'clouds': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'clouds_img': ('django.db.models.fields.CharField', [], {'default': "'na'", 'max_length': '3'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': "'2013-08-30 00:00'"}),
            'falls_img': ('django.db.models.fields.CharField', [], {'default': "'na'", 'max_length': '4'}),
            'humidity': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precipitation': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'max_length': '4'}),
            'pressure': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'temperature': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'wind_direction': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'wind_speed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'wp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['weather.WeatherProvider']"})
        },
        u'weather.weatherprovider': {
            'Meta': {'object_name': 'WeatherProvider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on_sidebar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'weather_city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'weather_provider': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'weather_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['weather']