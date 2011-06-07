__author__ = "hsk81"
__date__ = "$Jun 6, 2011 10:28:06 AM$"

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

    help = 'Multiplies to source pairs into a target pair'

    ###########################################################################
    ###########################################################################

    def check_pair (option, opt_str, value, parser):

        if value == None:
            raise OptionValueError("pair not set")

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
        
        make_option ('--lhs', '--lhs-pair',
            type='string',
            action='callback',
            dest='lhs_pair',
            callback=check_pair,
            help='left-hand-side fx pair to import with'
        ),

        make_option ('--rhs', '--rhs-pair',
            type='string',
            action='callback',
            dest='rhs_pair',
            callback=check_pair,
            help='right-hand-side fx pair to multiply with'
        ),

        make_option ('-f', '--file',
            type='string',
            action='store',
            dest='file',
            help='file to export to'
        ),

        make_option ('-s', '--start-datetime',
            action='callback',
            dest='start_datetime',
            callback=check_datetime,
            default=None,
            help='start datetime for source pairs [default: %default]'
        ),

        make_option ('-e', '--end-datetime',
            action='callback',
            dest='end_datetime',
            callback=check_datetime,
            default=None,
            help='end datetime for source pairs [default: %default]'
        ),
    )

    ###########################################################################
    ###########################################################################

    def handle(self, *args, **options):

        from core.models import PAIR, TICK
        
        logging.basicConfig (format='[%(asctime)s] %(levelname)s: %(message)s')
        srvlog_level = getattr (logging, options['srvlog_level'].upper(), None)
        if not isinstance (srvlog_level, int):
            
            raise CommandError ('invalid level: %s' % options['srvlog_level'])

        srvlog = logging.getLogger ('srv')
        srvlog.setLevel (srvlog_level)

        if options['file'] == None: raise CommandError ('FILE not set')
        else: filename = options['file']

        if options['lhs_pair'] == None: raise CommandError ('LHS_PAIR not set')
        else: lhs_q2b = options['lhs_pair']

        if options['rhs_pair'] == None: raise CommandError ('RHS_PAIR not set')
        else: rhs_q2b = options['rhs_pair']
        
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
                .values ()
        srvlog.debug ('start datetime is %s' % beg_datetime)

        srvlog.debug ('determining end datetime')
        if options['end_datetime'] != None:
            end_datetime = options['end_datetime']
        else:
            end_datetime = datetime.now ()
        srvlog.debug ('end datetime is %s' % end_datetime)

        srvlog.debug ('opening file "%s"' % filename)
        try: file = open (filename, 'w')
        except IOError as e: raise CommandError (e)

        with file:

            self.main (
                file, lhs_pair, rhs_pair, beg_datetime, end_datetime
            )
            
        srvlog.debug ('file "%s" closed' % filename)

    ###########################################################################
    ###########################################################################

    def main (self, file, lhs_pair, rhs_pair, beg_datetime, end_datetime):

        from core.models import PAIR, TICK
        
        srvlog = logging.getLogger ('srv')
        srvlog.info ('quote multiplication started')
        
        try:

        #######################################################################
        #######################################################################

            pass ## TODO!

        #######################################################################
        #######################################################################

        except KeyboardInterrupt:
            srvlog.info ('quote multiplication cancelled')

        except Exception, ex:
            srvlog.exception (ex)
            raise CommandError ('quote multiplication failed')

        #######################################################################
        #######################################################################

        srvlog.info ('quote multiplication done')

###############################################################################
###############################################################################
