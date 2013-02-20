# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Occurrence.event_date'
        db.alter_column('ants_atlas_occurrence', 'event_date', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Occurrence.event_date'
        raise RuntimeError("Cannot reverse this migration. 'Occurrence.event_date' and its values cannot be restored.")

    models = {
        'ants_atlas.mgrssquare': {
            'Meta': {'object_name': 'MGRSSquare'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'ants_atlas.occurrence': {
            'Meta': {'object_name': 'Occurrence'},
            'catalog_number': ('django.db.models.fields.IntegerField', [], {}),
            'event_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scientificname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'square': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.MGRSSquare']"})
        }
    }

    complete_apps = ['ants_atlas']