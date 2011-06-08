__author__ = "hsk81"
__date__ = "$May 29, 2011 5:15:44 PM$"

###############################################################################
###############################################################################

from django.core.management.base import *
from django.db.models import *
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

        make_option('-s', '--sliding-window',
            type='int',
            action='store',
            dest='buffer_size',
            default=4,
            help='size of sliding window to filter duplicates'
        ),
    )

    ###########################################################################
    ###########################################################################

    def handle(self, *args, **options):

        from core.models import PAIR, TICK

        logging.basicConfig (format='[%(asctime)s] %(levelname)s: %(message)s')
        srvlog_level = getattr(logging, options['srvlog_level'].upper(), None)
        if not isinstance (srvlog_level, int):
            
            raise CommandError ('invalid level: %s' % options['srvlog_level'])

        srvlog = logging.getLogger ('srv')
        srvlog.setLevel (srvlog_level)

        if options['file'] == None: raise CommandError ('FILE not set')
        else: filename = options['file']
        
        if options['pair'] == None: raise CommandError ('PAIR not set')
        else: q2b = options['pair']
        
        if options['buffer_size'] == None:
            raise CommandError ('BUFFER_SIZE not set')
        elif options['buffer_size'] <= 0:
            raise CommandError ('BUFFER_SIZE invalid')
        else:
            buffer_size = options['buffer_size']

        srvlog.debug ('querying for pair "%s"' % q2b)
        quote, base = q2b.split ('/')
        try: pair = PAIR.objects.get (quote=quote, base=base)
        except Exception as e: raise CommandError (e)

        srvlog.debug ('opening file "%s"' % filename)
        try: file = open (filename)
        except IOError as e: raise CommandError (e)

        with file:
            
            self.text2db (file, pair, buffer_size)
            
        srvlog.debug ('file "%s" closed' % filename)

    ###########################################################################
    ###########################################################################

    def text2db (self, file, pair, buffer_size):
        
        from core.models import PAIR, TICK

        srvlog = logging.getLogger ('srv')
        srvlog.info ('"%s" ticks\' import from "%s"' % (pair, file.name))

        try:
                        
            srvlog.info ('ticks\' import started')
            
            ###################################################################
            ###################################################################

            ticks = TICK.objects.filter (pair=pair)

            tmin, tmax = ticks \
                .aggregate (Min ('datetime'), Max ('datetime')) \
                .values ()

            ls = [None] * buffer_size ## last n lines to buffer

            ###################################################################
            for line in file:
            ###################################################################

                (d,t,b,a) = line.split (' '); dts = datetime.strptime (
                    '%s %s' % (d,t), '%d/%m/%y %H:%M:%S'
                )

                bid = Decimal (b)
                ask = Decimal (a)

                ###############################################################
                if tmin != None and dts < tmin: ## interval [:tmin]
                ###############################################################

                    TICK.objects.create (
                        pair=pair, datetime=dts, bid=bid, ask=ask
                    )

                    srvlog.debug ('%s << [++]' % line[:-1])

                ###############################################################
                elif tmax != None and dts <= tmax: ## interval [tmin:tmax]
                ###############################################################

                    ts = ticks.filter (datetime=dts, bid=bid, ask=ask)
                    ts_size = ts.count ()

                    if ts_size == 0: ## no ticks known yet;

                        TICK.objects.create (
                            pair=pair, datetime=dts, bid=bid, ask=ask
                        )

                        srvlog.debug ('%s :: [++]' % line[:-1])

                    else: ## is current tick a duplicate?

                        if ls.count (line) >= ts_size: ## looks genuine;

                            TICK.objects.create (pair=pair,
                                datetime=dts, bid=bid, ask=ask
                            )

                            srvlog.debug ('%s :: [&&]' % line[:-1])

                        else: ## seems to be an actual duplicate!

                            srvlog.debug ('%s :: [==]' % line[:-1])

                    ls.pop (0); ls.append (line)

                ###############################################################
                else: ## interval [tmax:]
                ###############################################################

                    TICK.objects.create (
                        pair=pair, datetime=dts, bid=bid, ask=ask
                    )

                    srvlog.debug ('%s >> [++]' % line[:-1])

            ###################################################################
            ###################################################################

            srvlog.info ('ticks\' import done')

        #######################################################################
        #######################################################################

        except KeyboardInterrupt:
            srvlog.info ('ticks\' import cancelled')

        except Exception, ex:
            srvlog.exception (ex)
            raise CommandError ('ticks\' import failed')

###############################################################################
###############################################################################
