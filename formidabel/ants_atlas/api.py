from tastypie.resources import ModelResource
from tastypie import fields

from ants_atlas.models import Occurrence, Species, MGRSSquare


class MGRSSquareResource(ModelResource):
    class Meta:
        queryset = MGRSSquare.objects.all()
        resource_name = 'square'


class SpeciesResource(ModelResource):
    occurrences = fields.ToManyField('ants_atlas.api.OccurrenceResource',
                                     'occurrence_set', related_name='species',
                                     full=True)

    class Meta:
        queryset = Species.objects.all()
        resource_name = 'species'


class OccurrenceResource(ModelResource):
    # Don't include species for performance
    # (we already access occurrences trough the species)
    square = fields.ForeignKey(MGRSSquareResource, 'square', full=True)

    class Meta:
        queryset = Occurrence.objects.all()
        resource_name = 'occurrence'
