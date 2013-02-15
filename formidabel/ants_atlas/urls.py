from django.conf.urls.defaults import *


urlpatterns = patterns('ants_atlas.views',
    url(r'^$', 'index', name="aa_main-view"),
)
