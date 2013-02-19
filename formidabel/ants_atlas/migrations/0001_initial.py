# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MGRSSquare'
        db.create_table('ants_atlas_mgrssquare', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('ants_atlas', ['MGRSSquare'])

        # Adding model 'Occurrence'
        db.create_table('ants_atlas_occurrence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('catalog_number', self.gf('django.db.models.fields.IntegerField')()),
            ('scientificname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('square', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ants_atlas.MGRSSquare'])),
        ))
        db.send_create_signal('ants_atlas', ['Occurrence'])


    def backwards(self, orm):
        # Deleting model 'MGRSSquare'
        db.delete_table('ants_atlas_mgrssquare')

        # Deleting model 'Occurrence'
        db.delete_table('ants_atlas_occurrence')


    models = {
        'ants_atlas.mgrssquare': {
            'Meta': {'object_name': 'MGRSSquare'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'ants_atlas.occurrence': {
            'Meta': {'object_name': 'Occurrence'},
            'catalog_number': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scientificname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'square': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.MGRSSquare']"})
        }
    }

    complete_apps = ['ants_atlas']