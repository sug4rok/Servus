# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Weather.wind_speed'
        db.alter_column(u'weather_weather', 'wind_speed', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=2))

        # Changing field 'Weather.clouds'
        db.alter_column(u'weather_weather', 'clouds', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=2))

        # Changing field 'Weather.temperature'
        db.alter_column(u'weather_weather', 'temperature', self.gf('django.db.models.fields.SmallIntegerField')(max_length=3))

        # Changing field 'Weather.wind_direction'
        db.alter_column(u'weather_weather', 'wind_direction', self.gf('django.db.models.fields.SmallIntegerField')(max_length=3))

        # Changing field 'Weather.pressure'
        db.alter_column(u'weather_weather', 'pressure', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=3))

        # Changing field 'Weather.humidity'
        db.alter_column(u'weather_weather', 'humidity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=2))

    def backwards(self, orm):

        # Changing field 'Weather.wind_speed'
        db.alter_column(u'weather_weather', 'wind_speed', self.gf('django.db.models.fields.IntegerField')(max_length=2))

        # Changing field 'Weather.clouds'
        db.alter_column(u'weather_weather', 'clouds', self.gf('django.db.models.fields.IntegerField')(max_length=2))

        # Changing field 'Weather.temperature'
        db.alter_column(u'weather_weather', 'temperature', self.gf('django.db.models.fields.IntegerField')(max_length=3))

        # Changing field 'Weather.wind_direction'
        db.alter_column(u'weather_weather', 'wind_direction', self.gf('django.db.models.fields.IntegerField')(max_length=3))

        # Changing field 'Weather.pressure'
        db.alter_column(u'weather_weather', 'pressure', self.gf('django.db.models.fields.IntegerField')(max_length=3))

        # Changing field 'Weather.humidity'
        db.alter_column(u'weather_weather', 'humidity', self.gf('django.db.models.fields.IntegerField')(max_length=2))

    models = {
        u'weather.weather': {
            'Meta': {'ordering': "('wp',)", 'object_name': 'Weather'},
            'clouds': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'max_length': '2'}),
            'clouds_img': ('django.db.models.fields.CharField', [], {'default': "'na'", 'max_length': '3'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': "'2013-08-30 00:00'"}),
            'falls_img': ('django.db.models.fields.CharField', [], {'default': "'na'", 'max_length': '4'}),
            'humidity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'precipitation': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'max_length': '4'}),
            'pressure': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'max_length': '3'}),
            'temperature': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'max_length': '3'}),
            'wind_direction': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'max_length': '3'}),
            'wind_speed': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'max_length': '2'}),
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