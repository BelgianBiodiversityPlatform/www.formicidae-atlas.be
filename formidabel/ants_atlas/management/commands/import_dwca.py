from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from ants_atlas.models import Occurrence, MGRSSquare, Family, Genus

from dwca import DwcAReader

def get_or_create_related_tuple(Model, column_name, value):
    try:
        keyword = column_name + "__exact"
        obj = Model.objects.get(**{keyword: value})
    except ObjectDoesNotExist:
        obj = Model()
        setattr(obj, column_name, value)
        obj.save()

    return obj

def truncate_all_tables():
    Occurrence.objects.all().delete()
    MGRSSquare.objects.all().delete()

def create_occurrence_from_dwcaline(line):
    #import pdb; pdb.set_trace()
    occ = Occurrence()

    # Simple fields
    # TODO: move these long Dwc strings to a specific module ?
    occ.catalog_number = line.get('http://rs.tdwg.org/dwc/terms/catalogNumber')
    occ.scientificname = line.get('http://rs.tdwg.org/dwc/terms/scientificName')
    event_date = line.get('http://rs.tdwg.org/dwc/terms/eventDate')
    if event_date != '':
        occ.event_date = event_date

    # Foreign keys
    mgrs_id = line.get('http://rs.tdwg.org/dwc/terms/verbatimCoordinates')
    occ.square = get_or_create_related_tuple(MGRSSquare, 'label', mgrs_id)

    family = line.get('http://rs.tdwg.org/dwc/terms/family')
    occ.family = get_or_create_related_tuple(Family, 'name', family)

    genus = line.get('http://rs.tdwg.org/dwc/terms/genus')
    if genus != '':
        occ.genus = get_or_create_related_tuple(Genus, 'name', genus)

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
            help='Truncate existing records before importing.'),

        make_option('--no-skip-first-line',
            action='store_false',
            dest='skip_fist_line',
            default=True,
            help='Skip first line of DwcA.'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Please give the path to the source DwcA.')
        else:
            source_filename = args[0]

            try:
                source = DwcAReader(source_filename)

                if options['truncate']:
                    self.stdout.write("Truncating existing records...")
                    truncate_all_tables()
                    self.stdout.write("Done.\n")

                lines = source.each_line()

                if options['skip_fist_line']:
                    next(lines)
                
                for l in lines:
                    self.stdout.write('.')
                    create_occurrence_from_dwcaline(l)

            except IOError as e:
                raise CommandError('Cannot open source DwcA: %s' % source_filename)


        
