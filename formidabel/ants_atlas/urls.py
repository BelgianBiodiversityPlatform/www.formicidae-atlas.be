from django.conf.urls.defaults import *
from tastypie.api import Api
from ants_atlas.api import (OccurrenceResource,
                            SpeciesResource, MGRSSquareResource)

v1_api = Api(api_name='v1')
v1_api.register(OccurrenceResource())
v1_api.register(SpeciesResource())
v1_api.register(MGRSSquareResource())

urlpatterns = patterns('ants_atlas.views',
    url(r'^$', 'index', name="aa_main-view"),
)

urlpatterns += patterns('',
    url(r'^api/', include(v1_api.urls))
)
