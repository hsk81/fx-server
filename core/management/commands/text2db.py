__author__ = "hsk81"
__date__ = "$May 29, 2011 5:15:44 PM$"

###############################################################################
###############################################################################

from django.core.management.base import *
from optparse import *
from datetime import *
from decimal import *

###############################################################################
###############################################################################

class Command (BaseCommand):

    help = 'Imports data into the foreign exchange server'

    def check_pair (option, opt_str, value, parser):

        if value == None:
            raise OptionValueError("pair not set")

        try: _, _ = value.split ('/')
        except: raise OptionValueError ("pair %s invalid" % value)

        setattr(parser.values, option.dest, value)

    option_list = BaseCommand.option_list + (
        make_option('-f', '--file',
            type='string',
            action='store',
            dest='file',
            help='Text file to import from'
        ),
        
        make_option('-p', '--pair',
            type='string',
            action='callback',
            dest='pair',
            callback=check_pair,
            help='FX pair to import for'
        ),
    )

    def handle(self, *args, **options):

        try:
            if options['file'] == None:
                raise OptionValueError ('FILE not set')
            if options['pair'] == None:
                raise OptionValueError ('PAIR not set')

        except OptionValueError as e:
            
            raise CommandError (e)
        
        else:
            self.text2db (options['pair'], options['file'])

    def text2db (self, quote2base, filename):

        from core.models import TICK
        from core.models import PAIR

        quote, base = quote2base.split ('/')        
        pairs = PAIR.objects.filter (quote=quote, base=base)
        if pairs.exists (): pair = pairs[0]
        else: raise CommandError ("no pair for %s" % quote2base)

        try: file = open (filename)
        except IOError as e: raise CommandError (e)

        with file:

            ##
            ## TODO: User logging instead of print >> self.stdout!
            ##
            
            print >> self.stdout, "importing ticks for %s from %s .." % (
                pair, filename
            )
            
            for line in file:

                (d,t,b,a) = line.split (' ')
                print >> self.stdout, (d,t,b,a)

                dts = datetime.strptime ('%s %s' % (d,t), '%d/%m/%y %H:%M:%S')
                bid = Decimal (b)
                ask = Decimal (a)

                TICK.objects.create (pair=pair, datetime=dts, bid=bid, ask=ask)

###############################################################################
###############################################################################
