__author__ = "hsk81"
__date__ = "$Jun 5, 2011 12:35:56 AM$"

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

    help = 'Removes data from the foreign exchange server'

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

        make_option('-a', '--all-ticks-per-line',
            action='store_true',
            dest='del_duplicates',
            default=False,
            help='causes all matching ticks per file line to be deleted'
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
        if options['del_duplicates'] == None:
            raise CommandError ('DEL_DUPLICATES not set')

        self.text2db (
            options['pair'], options['file'], options['del_duplicates']
        )

    ###########################################################################
    ###########################################################################

    def text2db (self, q2b, filename, del_duplicates):

        srvlog = logging.getLogger ('srv')
        srvlog.info ('"%s" ticks\' removal from "%s"' % (q2b, filename))

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
                srvlog.info ('ticks\' removal started')
                ticks = TICK.objects.filter (pair=pair)

                ###############################################################
                for line in file:
                ###############################################################

                    (d,t,b,a) = line.split (' '); dts = datetime.strptime (
                        '%s %s' % (d,t), '%d/%m/%y %H:%M:%S'
                    )

                    bid = Decimal (b)
                    ask = Decimal (a)

                    if del_duplicates:

                        ticks.filter (datetime=dts, bid=bid, ask=ask).delete ()
                        srvlog.debug ('%s :: [--]' % line[:-1])

                    else:

                        ts = ticks.filter (datetime=dts, bid=bid, ask=ask)
                        ts_size = ts.count ()

                        if ts_size == 0: ## no ticks found;

                            srvlog.debug ('%s :: [??]' % line[:-1])

                        else: ## delete only first tick;

                            for t in ts: t.delete (); break
                            srvlog.debug ('%s :: [--]' % line[:-1])

                ###############################################################
                ###############################################################

                srvlog.info ('ticks\' removal done')

            ###################################################################
            ###################################################################

            except KeyboardInterrupt:
                srvlog.info ('ticks\' removal cancelled')

            except Exception, ex:
                srvlog.exception (ex)
                raise CommandError ('ticks\' removal failed')

            ###################################################################
            ###################################################################

        srvlog.debug ('file "%s" closed' % filename)

###############################################################################
###############################################################################
