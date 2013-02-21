from tastypie.resources import ModelResource
from ants_atlas.models import Occurrence

class OccurrenceResource(ModelResource):
	class Meta:
		queryset = Occurrence.objects.all()
		resource_name = 'occurrence'

		