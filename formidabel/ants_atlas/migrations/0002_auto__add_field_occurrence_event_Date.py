# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Occurrence.event_Date'
        db.add_column('ants_atlas_occurrence', 'event_Date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 2, 20, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Occurrence.event_Date'
        db.delete_column('ants_atlas_occurrence', 'event_Date')


    models = {
        'ants_atlas.mgrssquare': {
            'Meta': {'object_name': 'MGRSSquare'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'ants_atlas.occurrence': {
            'Meta': {'object_name': 'Occurrence'},
            'catalog_number': ('django.db.models.fields.IntegerField', [], {}),
            'event_Date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scientificname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'square': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.MGRSSquare']"})
        }
    }

    complete_apps = ['ants_atlas']