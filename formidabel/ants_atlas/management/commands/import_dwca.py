from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from ants_atlas.models import Occurrence, MGRSSquare

from dwca import DwcAReader

def create_occurrence_from_dwcaline(line):
    #import pdb; pdb.set_trace()
    print '.'
    occ = Occurrence()

    # Simple fields
    # TODO: move these long Dwc strings to a specific module ?
    occ.catalog_number = line.get('http://rs.tdwg.org/dwc/terms/catalogNumber')
    occ.scientificname = line.get('http://rs.tdwg.org/dwc/terms/scientificName')

    # Foreign keys - MGRS square
    # TODO: Facorize this logic ?
    mgrs_id = line.get('http://rs.tdwg.org/dwc/terms/verbatimCoordinates')
    try:
        square = MGRSSquare.objects.get(label__exact=mgrs_id)
    except ObjectDoesNotExist: # If it soen't exists, let's create it !
        square = MGRSSquare()
        square.label = mgrs_id
        square.save()    

    occ.square = square
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
            raise CommandError('Please give the path to the source DwcA')
        else:
            source_filename = args[0]

            try:
                source = DwcAReader(source_filename)

                lines = source.each_line()

                if options['skip_fist_line']:
                    next(lines)
                
                for l in lines:
                    create_occurrence_from_dwcaline(l)

            except IOError as e:
                raise CommandError('Cannot open source DwcA: %s' % source_filename)

            if options['truncate']:
                self.stdout.write("Truncating existing records...")

        
