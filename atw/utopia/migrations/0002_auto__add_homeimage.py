# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HomeImage'
        db.create_table(u'utopia_homeimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='None', max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'utopia', ['HomeImage'])


    def backwards(self, orm):
        # Deleting model 'HomeImage'
        db.delete_table(u'utopia_homeimage')


    models = {
        u'utopia.episode': {
            'Meta': {'ordering': "['pub_date']", 'object_name': 'Episode'},
            'body': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'None'", 'max_length': '1024'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'utopia.homeimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'HomeImage'},
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'None'", 'max_length': '255'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
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