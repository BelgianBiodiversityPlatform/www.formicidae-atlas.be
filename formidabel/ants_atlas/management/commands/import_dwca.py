from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from ants_atlas.models import Occurrence, MGRSSquare, Family, Genus, Species

from dwca import DwCAReader
from dwca.darwincore.utils import qualname as qn


def get_or_create_taxonomy(family, genus, species, scientificname, specificepithet):
    # Let's start with the leaves, then go up, creating necessary instances on the fly
    f = Family.objects.get_or_create(name=family)[0]
    g = Genus.objects.get_or_create(name=genus, family=f)[0]

    return Species.objects.get_or_create(genus=g, scientificname=scientificname, specificepithet=specificepithet)[0]


def truncate_all_tables():
    models_to_truncate = [Occurrence, MGRSSquare, Family, Genus, Species]
    for model in models_to_truncate:
        model.objects.all().delete()


def create_occurrence_from_dwcaline(line):
    #import pdb; pdb.set_trace()
    occ = Occurrence()

    # Simple fields
    # TODO: move these long Dwc strings to a specific module ?
    occ.catalog_number = line.data[qn('catalogNumber')]
    occ.scientificname = ''  # TODO: Remove this field
    event_date = line.data[qn('eventDate')]
    if event_date != '':
        occ.event_date = event_date

    # Foreign keys
    mgrs_id = line.data[qn('verbatimCoordinates')]
    occ.square = MGRSSquare.objects.get_or_create(label=mgrs_id)[0]

    species = line.data[qn('specificEpithet')]
    genus = line.data[qn('genus')]
    family = line.data[qn('family')]
    scientificname = line.data[qn('scientificName')]
    specificepithet = line.data[qn('specificEpithet')]

    occ.species = get_or_create_taxonomy(family, genus, species,
                                         scientificname, specificepithet)

    occ.save()


# Should receive the path to source DwcA and an optional --truncate parameter
class Command(BaseCommand):
    args = '/path/to/dwca.zip'
    help = 'Import the Darwin Core Archive file to populate the Atlas of Ants.'

    option_list = BaseCommand.option_list + (
        make_option('--truncate',
                    action='store_true',
                    dest='truncate',
                    default=False,
                    help='Truncate existing records before importing.'),)

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please give the path to the source DwcA.')
        else:
            source_filename = args[0]

            try:
                source = DwCAReader(source_filename)

                if options['truncate']:
                    self.stdout.write("Truncating existing records...")
                    truncate_all_tables()
                    self.stdout.write("Done.\n")

                lines = source.each_line()

                for l in lines:
                    self.stdout.write('.')
                    create_occurrence_from_dwcaline(l)

            except IOError as e:
                raise CommandError('Cannot open source DwcA: %s' % source_filename)

