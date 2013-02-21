from django.db import models


class MGRSSquare(models.Model):
    label = models.CharField(max_length=16)


class Family(models.Model):
    name = models.CharField(max_length=50)


class Genus(models.Model):
    name = models.CharField(max_length=50)
    family = models.ForeignKey(Family, blank=True, null=True)


class Species(models.Model):
    scientificname = models.CharField(max_length=255)
    specificepithet = models.CharField(max_length=50)

    genus = models.ForeignKey(Genus, blank=True, null=True)


class Occurrence(models.Model):
    catalog_number = models.IntegerField()

    event_date = models.DateField(blank=True, null=True)

    species = models.ForeignKey(Species, blank=True, null=True)
    square = models.ForeignKey(MGRSSquare)
