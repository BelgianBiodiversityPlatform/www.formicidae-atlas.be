# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Genus'
        db.create_table('ants_atlas_genus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('ants_atlas', ['Genus'])

        # Adding model 'Family'
        db.create_table('ants_atlas_family', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('ants_atlas', ['Family'])

        # Adding field 'Occurrence.genus'
        db.add_column('ants_atlas_occurrence', 'genus',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ants_atlas.Genus'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Occurrence.family'
        db.add_column('ants_atlas_occurrence', 'family',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ants_atlas.Family'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Genus'
        db.delete_table('ants_atlas_genus')

        # Deleting model 'Family'
        db.delete_table('ants_atlas_family')

        # Deleting field 'Occurrence.genus'
        db.delete_column('ants_atlas_occurrence', 'genus_id')

        # Deleting field 'Occurrence.family'
        db.delete_column('ants_atlas_occurrence', 'family_id')


    models = {
        'ants_atlas.family': {
            'Meta': {'object_name': 'Family'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ants_atlas.genus': {
            'Meta': {'object_name': 'Genus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ants_atlas.mgrssquare': {
            'Meta': {'object_name': 'MGRSSquare'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'ants_atlas.occurrence': {
            'Meta': {'object_name': 'Occurrence'},
            'catalog_number': ('django.db.models.fields.IntegerField', [], {}),
            'event_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.Family']", 'null': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.Genus']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scientificname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'square': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.MGRSSquare']"})
        }
    }

    complete_apps = ['ants_atlas']