from django.shortcuts import render

from ants_atlas.models import Genus
from formidabel.settings import ANTSATLAS_CONFIG


def index(request):
    template_vars = {
        'genus': Genus.objects.all(),
        'config': ANTSATLAS_CONFIG
    }

    return render(request, 'index.html', template_vars)
