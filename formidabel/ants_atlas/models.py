from django.db import models


class MGRSSquare(models.Model):
    label = models.CharField(max_length=16)


class Occurrence(models.Model):
    catalog_number = models.IntegerField()
    scientificname = models.CharField(max_length=255)
    square = models.ForeignKey(MGRSSquare)
