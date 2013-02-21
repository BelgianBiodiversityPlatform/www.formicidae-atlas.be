from django.conf.urls.defaults import *
from ants_atlas.api import OccurrenceResource

occurrence_resource = OccurrenceResource()

urlpatterns = patterns('ants_atlas.views',
    url(r'^$', 'index', name="aa_main-view"),
    url(r'^api/', include(occurrence_resource.urls))
)
