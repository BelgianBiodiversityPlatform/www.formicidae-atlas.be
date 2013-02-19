# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Kaste(models.Model):
    id = models.IntegerField(primary_key=True, db_column='Id') # Field name made lowercase.
    kaste = models.TextField(db_column='Kaste', blank=True) # Field name made lowercase.
    afkorting = models.TextField(db_column='Afkorting', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Kaste'

class InCollectie(models.Model):
    opgenomen = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'In collectie'

class Determinator(models.Model):
    code = models.TextField(primary_key=True)
    naam = models.TextField(blank=True)
    class Meta:
        db_table = u'Determinator'

class Ecocode(models.Model):
    id = models.IntegerField(null=True, db_column='ID', blank=True) # Field name made lowercase.
    ecocode = models.TextField(primary_key=True)
    landschap = models.TextField(blank=True)
    definitie = models.TextField(blank=True)
    class Meta:
        db_table = u'Ecocode'

