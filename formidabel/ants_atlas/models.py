from django.db import models


class MGRSSquare(models.Model):
    label = models.CharField(max_length=16)


class Genus(models.Model):
    name = models.CharField(max_length=50)


class Family(models.Model):
    name = models.CharField(max_length=50)


class Occurrence(models.Model):
    catalog_number = models.IntegerField()
    scientificname = models.CharField(max_length=255)

    event_date = models.DateField(blank=True, null=True)

    genus = models.ForeignKey(Genus, blank=True, null=True)
    family = models.ForeignKey(Family, blank=True, null=True)

    square = models.ForeignKey(MGRSSquare)
