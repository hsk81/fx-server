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
        if options['buffer_size'] == None:
            raise CommandError ('BUFFER_SIZE not set')
        if options['buffer_size'] == 0:
            raise CommandError ('BUFFER_SIZE invalid')

        self.text2db (
            options['pair'], options['file'], options['buffer_size']
        )

    ###########################################################################
    ###########################################################################

    def text2db (self, q2b, filename, buffer_size, del_duplicates=False):

        srvlog = logging.getLogger ('srv')
        srvlog.info ('"%s" ticks\' import from "%s"' % (q2b, filename))

        from core.models import TICK
        from core.models import PAIR

        srvlog.debug ('querying for pair "%s"' % q2b)
        quote, base = q2b.split ('/')
        pairs = PAIR.objects.filter (quote=quote, base=base)
        if pairs.exists (): pair = pairs[0]
        else: raise CommandError ('no pair for "%s"' % q2b)

        srvlog.debug ('opening file "%s"' % filename)
        try: file = open (filename)
        except IOError as e: raise CommandError (e)

        #######################################################################
        with file:
        #######################################################################

            try:
                srvlog.info ('ticks\' import started')
                ticks = TICK.objects.filter (pair=pair)

                tmin, tmax = ticks \
                    .aggregate (Min ('datetime'), Max ('datetime')) \
                    .values ()

                ls = [None] * buffer_size ## last n lines to buffer

                ###############################################################
                for line in file:
                ###############################################################

                    (d,t,b,a) = line.split (' '); dts = datetime.strptime (
                        '%s %s' % (d,t), '%d/%m/%y %H:%M:%S'
                    )

                    bid = Decimal (b)
                    ask = Decimal (a)

                    ###########################################################
                    if tmin != None and dts < tmin: ## interval [:tmin]
                    ###########################################################

                        TICK.objects.create (
                            pair=pair, datetime=dts, bid=bid, ask=ask
                        )

                        srvlog.debug ('%s << [++]' % line[:-1])

                    ###########################################################
                    elif tmax != None and dts <= tmax: ## interval [tmin:tmax]
                    ###########################################################

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

                    ###########################################################
                    else: ## interval [tmax:]
                    ###########################################################

                        TICK.objects.create (
                            pair=pair, datetime=dts, bid=bid, ask=ask
                        )

                        srvlog.debug ('%s >> [++]' % line[:-1])

                ###############################################################
                ###############################################################

                srvlog.info ('ticks\' import done')

            ###################################################################
            ###################################################################

            except KeyboardInterrupt:
                srvlog.info ('ticks\' import cancelled')

            except Exception, ex:
                srvlog.exception (ex)
                raise CommandError ('ticks\' import failed')

            ###################################################################
            ###################################################################

        srvlog.debug ('file "%s" closed' % filename)

###############################################################################
###############################################################################
