from django.shortcuts import render

from ants_atlas.models import Genus


def index(request):
    return render(request, 'index.html', {'genus': Genus.objects.all()})
