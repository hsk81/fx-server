__author__ = "hsk81"
__date__ = "$Jun 5, 2011 12:35:56 AM$"

###############################################################################
###############################################################################

from django.core.management.base import *
from django.db.models import *
from optparse import *
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

    ###########################################################################
    ###########################################################################

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

    def handle (self, *args, **options):
        
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

        if options['del_duplicates'] == None:
            raise CommandError ('DEL_DUPLICATES not set')
        else:
            del_duplicates = options['del_duplicates']

        srvlog.debug ('querying for pair "%s"' % q2b)
        quote, base = q2b.split ('/')
        try: pair = PAIR.objects.get (quote=quote, base=base)
        except Exception as e: raise CommandError (e)

        srvlog.debug ('opening file "%s"' % filename)
        try: file = open (filename)
        except IOError as e: raise CommandError (e)

        with file:
            
            self.delete (file, pair, del_duplicates)

        srvlog.debug ('file "%s" closed' % filename)
        
    ###########################################################################
    ###########################################################################

    def delete (self, file, pair, del_duplicates):

        from core.models import PAIR, TICK

        srvlog = logging.getLogger ('srv')
        srvlog.info ('"%s" ticks\' remove from "%s"' % (pair, file.name))
        
        try:
            
            srvlog.info ('ticks\' remove started')

            ###################################################################
            ###################################################################

            ticks = TICK.objects.filter (pair=pair)

            ###################################################################
            for line in file:
            ###################################################################

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

        #######################################################################
        #######################################################################

        except KeyboardInterrupt:
            
            srvlog.debug ('transaction rollback started')
            transaction.rollback ()
            srvlog.debug ('transaction rollback stopped')
            srvlog.info ('ticks\' remove cancelled')

        except Exception, ex:

            srvlog.debug ('transaction rollback started')
            transaction.rollback ()
            srvlog.debug ('transaction rollback stopped')

            srvlog.exception (ex); raise CommandError (
                'ticks\' remove crashed'
            )

        else:
            
            srvlog.debug ('transaction commit started')
            transaction.commit ()
            srvlog.debug ('transaction commit stopped')
            srvlog.info ('ticks\' remove stopped')

###############################################################################
###############################################################################
