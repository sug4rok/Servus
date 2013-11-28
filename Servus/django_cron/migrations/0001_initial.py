# coding=utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CronJobLog'
        db.create_table(u'django_cron_cronjoblog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('is_success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
            ('ran_at_time', self.gf('django.db.models.fields.TimeField')(db_index=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'django_cron', ['CronJobLog'])

        # Adding index on 'CronJobLog', fields ['code', 'is_success', 'ran_at_time']
        db.create_index(u'django_cron_cronjoblog', ['code', 'is_success', 'ran_at_time'])

        # Adding index on 'CronJobLog', fields ['code', 'start_time', 'ran_at_time']
        db.create_index(u'django_cron_cronjoblog', ['code', 'start_time', 'ran_at_time'])

        # Adding index on 'CronJobLog', fields ['code', 'start_time']
        db.create_index(u'django_cron_cronjoblog', ['code', 'start_time'])


    def backwards(self, orm):
        # Removing index on 'CronJobLog', fields ['code', 'start_time']
        db.delete_index(u'django_cron_cronjoblog', ['code', 'start_time'])

        # Removing index on 'CronJobLog', fields ['code', 'start_time', 'ran_at_time']
        db.delete_index(u'django_cron_cronjoblog', ['code', 'start_time', 'ran_at_time'])

        # Removing index on 'CronJobLog', fields ['code', 'is_success', 'ran_at_time']
        db.delete_index(u'django_cron_cronjoblog', ['code', 'is_success', 'ran_at_time'])

        # Deleting model 'CronJobLog'
        db.delete_table(u'django_cron_cronjoblog')


    models = {
        u'django_cron.cronjoblog': {
            'Meta': {'object_name': 'CronJobLog', 'index_together': "[('code', 'is_success', 'ran_at_time'), ('code', 'start_time', 'ran_at_time'), ('code', 'start_time')]"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_success': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'ran_at_time': ('django.db.models.fields.TimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['django_cron']