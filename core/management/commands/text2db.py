__author__ = "hsk81"
__date__ = "$May 29, 2011 5:15:44 PM$"

###############################################################################
###############################################################################

from django.core.management.base import *
from datetime import *
from decimal import *

import logging

###############################################################################
###############################################################################

class Command (BaseCommand):

    ###########################################################################
    ###########################################################################

    help = 'Imports data into the foreign exchange server'

    ###########################################################################
    ###########################################################################

    def check_pair (option, opt_str, value, parser):

        if value == None:
            raise OptionValueError("pair not set")

        try: _, _ = value.split ('/')
        except: raise OptionValueError ("pair %s invalid" % value)

        setattr(parser.values, option.dest, value)

    option_list = BaseCommand.option_list + (
        make_option ('-l', '--general-log-level',
            type='string',
            action='store',
            dest='srvlog_level',
            default='info',
            help='server\'s general log level [default: %default]'
        ),
        
        make_option('-f', '--file',
            type='string',
            action='store',
            dest='file',
            help='text file to import from'
        ),

        make_option('-p', '--pair',
            type='string',
            action='callback',
            dest='pair',
            callback=check_pair,
            help='fx pair to import for'
        ),

        make_option('-i', '--import-duplicates',
            action='store_true',
            dest='import_duplicates',
            default=False,
            help='duplicate ticks are also imported'
        ),
    )

    ###########################################################################
    ###########################################################################

    def handle(self, *args, **options):

        logging.basicConfig (format='[%(asctime)s] %(levelname)s: %(message)s')

        srvlog_level = getattr(logging, options['srvlog_level'].upper(), None)
        if not isinstance(srvlog_level, int):
            raise CommandError('invalid level: %s' % options['srvlog_level'])

        srvlog = logging.getLogger ('srv')
        srvlog.setLevel (srvlog_level)

        if options['file'] == None:
            raise CommandError ('FILE not set')
        if options['pair'] == None:
            raise CommandError ('PAIR not set')

        self.text2db (
            options['pair'], options['file'], options['import_duplicates']
        )

    ###########################################################################
    ###########################################################################

    def text2db (self, quote2base, filename, import_duplicates):

        srvlog = logging.getLogger ('srv')
        srvlog.info ('"%s" ticks\' import from "%s"' % (quote2base, filename))

        from core.models import TICK
        from core.models import PAIR

        srvlog.debug ('querying for pair "%s"' % quote2base)
        quote, base = quote2base.split ('/')        
        pairs = PAIR.objects.filter (quote=quote, base=base)
        if pairs.exists (): pair = pairs[0]
        else: raise CommandError ('no pair for "%s"' % quote2base)

        srvlog.debug ('opening file "%s"' % filename)
        try: file = open (filename)
        except IOError as e: raise CommandError (e)

        with file:
            srvlog.info ('ticks\' import started')

            try:
                if import_duplicates:
                    srvlog.info ('importing duplicate ticks')
                    for line in file:

                        (d,t,b,a) = line.split (' '); dts = datetime.strptime (
                            '%s %s' % (d,t), '%d/%m/%y %H:%M:%S'
                        )

                        bid = Decimal (b)
                        ask = Decimal (a)

                        TICK.objects.create (
                            pair=pair, datetime=dts, bid=bid, ask=ask
                        )

                        srvlog.debug ('%s [ok]' % line[:-1])

                    srvlog.info ('ticks\' import (with duplicates) done')

                else:
                    srvlog.info ('ignoring duplicate ticks')
                    for line in file:

                        (d,t,b,a) = line.split (' '); dts = datetime.strptime (
                            '%s %s' % (d,t), '%d/%m/%y %H:%M:%S'
                        )

                        bid = Decimal (b)
                        ask = Decimal (a)

                        ts = TICK.objects.filter (
                            pair=pair, datetime=dts, bid=bid, ask=ask
                        )

                        if not ts.exists ():

                            TICK.objects.create (
                                pair=pair, datetime=dts, bid=bid, ask=ask
                            )

                            srvlog.debug ('%s [ok]' % line[:-1])

                        else:

                            srvlog.debug ('%s [!!]' % line[:-1])

                    srvlog.info ('ticks\' import (without duplicates) done')

            except KeyboardInterrupt:
                srvlog.info ('ticks\' import cancelled')

            except Exception, ex:
                srvlog.exception (ex)
                raise CommandError ('ticks\' import failed')

        srvlog.debug ('file "%s" closed' % filename)

###############################################################################
###############################################################################
