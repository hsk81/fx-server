__author__ = "hsk81"
__date__ = "$Jun 6, 2011 10:28:06 AM$"

###############################################################################
###############################################################################

from django.core.management.base import *
from django.db.models import *
from datetime import *
from decimal import *
from random import *

import logging
import sys

###############################################################################
###############################################################################

class Command (BaseCommand):

    ###########################################################################
    ###########################################################################

    help = 'Export a target pair directly or from two source pairs'

    ###########################################################################
    ###########################################################################

    def check_pair (option, opt_str, value, parser):

        if value != None:

            try: _, _ = value.split ('/')
            except: raise OptionValueError ("pair '%s' invalid" % value)

        setattr(parser.values, option.dest, value)

    def check_datetime (option, opt_str, value, parser):

        if value != None:

            try: result = datetime.strptime (value, '%Y-%m-%d %H:%M:%S')
            except ValueError as e: raise OptionValueError (e)

        else: result = None

        setattr(parser.values, option.dest, result)

    option_list = BaseCommand.option_list + (
        make_option ('-l', '--general-log-level',
            type='string',
            action='store',
            dest='srvlog_level',
            default='info',
            help='server\'s general log level [default: %default]'
        ),
        
        make_option ('-p', '--pair',
            type='string',
            action='callback',
            dest='tar_pair',
            callback=check_pair,
            default=None,
            help='target fx pair to export for [default: %default]'
        ),

        make_option ('--lhs', '--lhs-pair',
            type='string',
            action='callback',
            dest='lhs_pair',
            callback=check_pair,
            default=None,
            help='left-hand-side fx pair to export for [default: %default]'
        ),

        make_option ('--rhs', '--rhs-pair',
            type='string',
            action='callback',
            dest='rhs_pair',
            callback=check_pair,
            default=None,
            help='right-hand-side fx pair to export for [default: %default]'
        ),

        make_option ('--lhs-likelihood',
            action='store',
            dest='lhs_likelihood',
            default=None,
            help='likelihood to export for the lhs pair [default: %default]'
        ),

        make_option ('--rhs-likelihood',
            action='store',
            dest='rhs_likelihood',
            default=None,
            help='likelihood to export for the rhs pair [default: %default]'
        ),

        make_option ('-f', '--file',
            type='string',
            action='store',
            dest='file',
            default=None,
            help='file to export to [default: %default]'
        ),

        make_option ('-s', '--start-datetime',
            action='callback',
            dest='start_datetime',
            callback=check_datetime,
            default=None,
            help='start datetime for pairs [default: %default]'
        ),

        make_option ('-e', '--end-datetime',
            action='callback',
            dest='end_datetime',
            callback=check_datetime,
            default=None,
            help='end datetime for pairs [default: %default]'
        ),

        make_option ('-g','--prg-seed',
            type='int',
            action='store',
            dest='seed',
            default=31,
            help='seed for pseudo random generator [default: %default]'
        ),
    )

    ###########################################################################
    def handle (self, *args, **options):
    ###########################################################################

        logging.basicConfig (format='[%(asctime)s] %(levelname)s: %(message)s')
        srvlog_level = getattr (logging, options['srvlog_level'].upper(), None)
        if not isinstance (srvlog_level, int):

            raise CommandError ('invalid level: %s' % options['srvlog_level'])

        srvlog = logging.getLogger ('srv')
        srvlog.setLevel (srvlog_level)

        if options['tar_pair'] != None:
            self.handle_export (*args, **options)
        else: 
            self.handle_lhsrhs (*args, **options)

    ###########################################################################
    def handle_export (self, *args, **options):
    ###########################################################################

        from core.models import PAIR, TICK
        srvlog = logging.getLogger ('srv')

        if options['file'] == None: filename = sys.stdout.name
        else: filename = options['file']

        if options['tar_pair'] == None: raise CommandError ('TAR_PAIR not set')
        else: tar_q2b = options['tar_pair']

        srvlog.debug ('querying for pair "%s"' % tar_q2b)
        tar_quote, tar_base = tar_q2b.split ('/')
        try: tar_pair = PAIR.objects.get (quote=tar_quote, base=tar_base)
        except Exception as e: raise CommandError (e)

        srvlog.debug ('determining start datetime')
        if options['start_datetime'] != None:
            beg_datetime = options['start_datetime']
        else:
            beg_datetime = TICK.objects.filter (pair=tar_pair) \
                .aggregate (Min ('datetime')) \
                .values ()[0] or datetime.min

        srvlog.debug ('determining end datetime')
        if options['end_datetime'] != None:
            end_datetime = options['end_datetime']
        else:
            end_datetime = datetime.max
        

        srvlog.debug ('opening file "%s"' % filename)
        try: file = (filename != sys.stdout.name) and open (filename, 'w') \
            or sys.stdout
        except IOError as e: raise CommandError (e)

        with file:

            self.export (file,
                tar_pair, {'beg':beg_datetime, 'end':end_datetime}
            )

        srvlog.debug ('file "%s" closed' % filename)

    ###########################################################################
    def export (self, file, tar_pair, interval):
    ###########################################################################

        from core.models import PAIR, TICK
        srvlog = logging.getLogger ('srv')
        srvlog.info ('export for "%s" started' % tar_pair)

        beg_datetime = interval['beg']
        srvlog.info ('interval from: %s' % beg_datetime)
        end_datetime = interval['end'];
        srvlog.info ('interval till: %s' % end_datetime)

        try:

            tar_ticks = TICK.objects.filter (pair=tar_pair,
                datetime__gte=beg_datetime, datetime__lt=end_datetime
            )

            ###################################################################
            for tar_tick in tar_ticks:
            ###################################################################

                tar_dts = tar_tick.datetime.strftime ('%d/%m/%y %H:%M:%S')
                tar_bid = '%0.6f' % tar_tick.bid
                tar_ask = '%0.6f' % tar_tick.ask
                tar_str = '%s %s %s' % (tar_dts, tar_bid, tar_ask)

                print >> file, tar_str; srvlog.debug (tar_str)

        #######################################################################
        #######################################################################

        except KeyboardInterrupt:
            srvlog.info ('export for "%s" cancelled' % tar_pair)

        except StopIteration, ex:
            srvlog.debug ('iteration stopped')
            srvlog.info ('export for "%s" done' % tar_pair)

        except Exception, ex:
            srvlog.exception (ex)
            srvlog.info ('export for "%s" failed' % tar_pair)

    ###########################################################################
    def handle_lhsrhs (self, *args, **options):
    ###########################################################################

        from core.models import PAIR, TICK        
        srvlog = logging.getLogger ('srv')

        if options['file'] == None: filename = sys.stdout.name
        else: filename = options['file']

        if options['lhs_pair'] == None: raise CommandError ('LHS_PAIR not set')
        else: lhs_q2b = options['lhs_pair']
        if options['rhs_pair'] == None: raise CommandError ('RHS_PAIR not set')
        else: rhs_q2b = options['rhs_pair']

        if options['lhs_likelihood'] == None: lhs_likelihood = None
        else: lhs_likelihood = float (options['lhs_likelihood'])
        if options['rhs_likelihood'] == None: rhs_likelihood = None
        else: rhs_likelihood = float (options['rhs_likelihood'])

        if options['seed'] == None: raise CommandError ('SEED not set')
        else: seed (options['seed'])

        lhs_quote, lhs_base = lhs_q2b.split ('/')
        rhs_quote, rhs_base = rhs_q2b.split ('/')

        if lhs_base != rhs_quote:

            raise CommandError ('pairs "%s" and "%s" do not match' % \
                (lhs_q2b, rhs_q2b)
            )

        srvlog.debug ('querying for pair "%s"' % lhs_q2b)
        try: lhs_pair = PAIR.objects.get (quote=lhs_quote, base=lhs_base)
        except Exception as e: raise CommandError (e)

        srvlog.debug ('querying for pair "%s"' % rhs_q2b)
        try: rhs_pair = PAIR.objects.get (quote=rhs_quote, base=rhs_base)
        except Exception as e: raise CommandError (e)

        srvlog.debug ('querying for pair "%s/%s"' % (lhs_quote, rhs_base))
        try: tar_pair = PAIR.objects.get (quote=lhs_quote, base=rhs_base)
        except Exception as e: raise CommandError (e)

        srvlog.debug ('determining start datetime')
        if options['start_datetime'] != None:
            beg_datetime = options['start_datetime']
        else:
            beg_datetime = TICK.objects.filter (pair=tar_pair) \
                .aggregate (Max ('datetime')) \
                .values ()[0] or datetime.min

        srvlog.debug ('determining end datetime')
        if options['end_datetime'] != None:
            end_datetime = options['end_datetime']
        else:
            end_datetime = datetime.max

        srvlog.debug ('opening file "%s"' % filename)
        try: file = filename != sys.stdout.name and open (filename, 'w') \
            or sys.stdout
        except IOError as e: raise CommandError (e)

        with file:

            self.lhsrhs (file,
                {'lhs':lhs_pair, 'rhs':rhs_pair},
                {'lhs':lhs_likelihood, 'rhs':rhs_likelihood},
                {'beg':beg_datetime, 'end':end_datetime}
            )
            
        srvlog.debug ('file "%s" closed' % filename)

    ###########################################################################
    def lhsrhs (self, file, pairs, thresholds, interval):
    ###########################################################################

        from core.models import PAIR, TICK
        
        lhs_pair = pairs['lhs']; lhs_likelihood = thresholds['lhs']
        rhs_pair = pairs['rhs']; rhs_likelihood = thresholds['rhs']
        
        srvlog = logging.getLogger ('srv'); srvlog.info (
            u'export for "%s \u00D7 %s" started' % (lhs_pair, rhs_pair)
        )

        beg_datetime = interval['beg']
        srvlog.info ('interval from: %s' % beg_datetime)
        end_datetime = interval['end']
        srvlog.info ('interval till: %s' % end_datetime)
        
        try:

            lhs_ticks = TICK.objects.filter (pair=lhs_pair,
                datetime__gte=beg_datetime, datetime__lt=end_datetime
            )

            lhs_count = lhs_ticks.count ()
            lhs_ticks = lhs_ticks.iterator ()

            rhs_ticks = TICK.objects.filter (pair=rhs_pair,
                datetime__gte=beg_datetime, datetime__lt=end_datetime
            )

            rhs_count = rhs_ticks.count ()
            rhs_ticks = rhs_ticks.iterator ()

            if lhs_likelihood == None:
                lhs_likelihood = 1.0*lhs_count/(lhs_count+rhs_count)
            if rhs_likelihood == None:
                rhs_likelihood = 1.0*rhs_count/(lhs_count+rhs_count)

            lhs_tick = lhs_ticks.next ()
            rhs_tick = rhs_ticks.next ()

            ###################################################################
            while True:
            ###################################################################

                tar_bid = '%0.6f' % (lhs_tick.bid * rhs_tick.bid)
                tar_ask = '%0.6f' % (lhs_tick.ask * rhs_tick.ask)

                lhs_dts = lhs_tick.datetime
                rhs_dts = rhs_tick.datetime

                if lhs_tick.datetime < rhs_tick.datetime:

                    tar_dts = lhs_dts + (rhs_dts - lhs_dts) / 2
                    tar_dts = tar_dts.strftime ('%d/%m/%y %H:%M:%S')
                    tar_str = '%s %s %s' % (tar_dts, tar_bid, tar_ask)

                    if random () <= lhs_likelihood:

                        print >> file, tar_str; srvlog.debug (
                            '%s L [%s]' % (tar_str, lhs_pair)
                        )

                    lhs_tick = lhs_ticks.next ()

                else:

                    tar_dts = rhs_dts + (lhs_dts - rhs_dts) / 2
                    tar_dts = tar_dts.strftime ('%d/%m/%y %H:%M:%S')
                    tar_str = '%s %s %s' % (tar_dts, tar_bid, tar_ask)
                    
                    if random () <= rhs_likelihood:

                        print >> file, tar_str; srvlog.debug (
                            '%s R [%s]' % (tar_str, rhs_pair)
                        )

                    rhs_tick = rhs_ticks.next ()

        #######################################################################
        #######################################################################

        except KeyboardInterrupt:
            srvlog.info (
                u'export for "%s \u00D7 %s" cancelled' % (lhs_pair, rhs_pair)
            )

        except StopIteration, ex:
            srvlog.debug ('iteration stopped'); srvlog.info (
                u'export for "%s \u00D7 %s" done' % (lhs_pair,rhs_pair)
            )

        except Exception, ex:
            srvlog.exception (ex); srvlog.info (
                u'export for "%s \u00D7 %s" failed' % (lhs_pair, rhs_pair)
            )

###############################################################################
###############################################################################
