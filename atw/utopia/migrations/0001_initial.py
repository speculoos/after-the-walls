# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Media'
        db.create_table(u'utopia_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='None', max_length=1024)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('resource', self.gf('django.db.models.fields.files.FileField')(max_length=500)),
            ('episode', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['utopia.Episode'], null=True, blank=True)),
        ))
        db.send_create_signal(u'utopia', ['Media'])

        # Adding model 'Episode'
        db.create_table(u'utopia_episode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='None', max_length=1024)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('body', self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'utopia', ['Episode'])


    def backwards(self, orm):
        # Deleting model 'Media'
        db.delete_table(u'utopia_media')

        # Deleting model 'Episode'
        db.delete_table(u'utopia_episode')


    models = {
        u'utopia.episode': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Episode'},
            'body': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'None'", 'max_length': '1024'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'utopia.media': {
            'Meta': {'ordering': "['name']", 'object_name': 'Media'},
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['utopia.Episode']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'resource': ('django.db.models.fields.files.FileField', [], {'max_length': '500'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'None'", 'max_length': '1024'})
        }
    }

    complete_apps = ['utopia']