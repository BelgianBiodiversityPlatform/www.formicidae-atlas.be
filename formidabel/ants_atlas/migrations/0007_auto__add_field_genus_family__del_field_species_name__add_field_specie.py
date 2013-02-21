# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Genus.family'
        db.add_column('ants_atlas_genus', 'family',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ants_atlas.Family'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Species.name'
        db.delete_column('ants_atlas_species', 'name')

        # Adding field 'Species.scientificname'
        db.add_column('ants_atlas_species', 'scientificname',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Species.genus'
        db.add_column('ants_atlas_species', 'genus',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ants_atlas.Genus'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Occurrence.scientificname'
        db.delete_column('ants_atlas_occurrence', 'scientificname')

        # Deleting field 'Occurrence.family'
        db.delete_column('ants_atlas_occurrence', 'family_id')

        # Deleting field 'Occurrence.genus'
        db.delete_column('ants_atlas_occurrence', 'genus_id')


    def backwards(self, orm):
        # Deleting field 'Genus.family'
        db.delete_column('ants_atlas_genus', 'family_id')


        # User chose to not deal with backwards NULL issues for 'Species.name'
        raise RuntimeError("Cannot reverse this migration. 'Species.name' and its values cannot be restored.")
        # Deleting field 'Species.scientificname'
        db.delete_column('ants_atlas_species', 'scientificname')

        # Deleting field 'Species.genus'
        db.delete_column('ants_atlas_species', 'genus_id')


        # User chose to not deal with backwards NULL issues for 'Occurrence.scientificname'
        raise RuntimeError("Cannot reverse this migration. 'Occurrence.scientificname' and its values cannot be restored.")
        # Adding field 'Occurrence.family'
        db.add_column('ants_atlas_occurrence', 'family',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ants_atlas.Family'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Occurrence.genus'
        db.add_column('ants_atlas_occurrence', 'genus',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ants_atlas.Genus'], null=True, blank=True),
                      keep_default=False)


    models = {
        'ants_atlas.family': {
            'Meta': {'object_name': 'Family'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ants_atlas.genus': {
            'Meta': {'object_name': 'Genus'},
            'family': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.Family']", 'null': 'True', 'blank': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.Species']", 'null': 'True', 'blank': 'True'}),
            'square': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.MGRSSquare']"})
        },
        'ants_atlas.species': {
            'Meta': {'object_name': 'Species'},
            'genus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ants_atlas.Genus']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scientificname': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['ants_atlas']