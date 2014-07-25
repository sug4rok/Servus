# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SlideshowChanges'
        db.create_table(u'slideshow_slideshowchanges', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mtime', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'slideshow', ['SlideshowChanges'])

        # Adding model 'Slideshow'
        db.create_table(u'slideshow_slideshow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album_path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('is_shown', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'slideshow', ['Slideshow'])


    def backwards(self, orm):
        # Deleting model 'SlideshowChanges'
        db.delete_table(u'slideshow_slideshowchanges')

        # Deleting model 'Slideshow'
        db.delete_table(u'slideshow_slideshow')


    models = {
        u'slideshow.slideshow': {
            'Meta': {'object_name': 'Slideshow'},
            'album_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_shown': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'slideshow.slideshowchanges': {
            'Meta': {'object_name': 'SlideshowChanges'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mtime': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        }
    }

    complete_apps = ['slideshow']