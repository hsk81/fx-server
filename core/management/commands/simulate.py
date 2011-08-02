__author__ = "hsk81"
__date__ = "$Jun 22, 2011 1:26:13 AM$"

###############################################################################
###############################################################################

from optparse import *
from datetime import *
from django.core.management.base import *

import zmq
import time
import logging

###############################################################################
###############################################################################

class Command (BaseCommand):

    ###########################################################################
    ###########################################################################

    help = 'Runs the foreign exchange server\'s rate publisher service'

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
            except ValueError as e: raise OptionValueError ('%s' % e)

        else: result = None

        setattr(parser.values, option.dest, result)

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
        
        make_option ('-m', '--message-log-level',
            type='string',
            action='store',
            dest='msglog_level',
            default='info',
            help='server\'s message log level [default: %default]'
        ),

        make_option ('-p', '--pair',
            type='string',
            action='callback',
            dest='tar_pair',
            callback=check_pair,
            default=None,
            help='target fx pair to publish for [default: %default]'
        ),

        make_option ('-b', '--beg-datetime',
            type='string',
            action='callback',
            dest='beg_datetime',
            callback=check_datetime,
            default=None,
            help='beg datetime for interval [default: %default]'
        ),

        make_option ('-e', '--end-datetime',
            type='string',
            action='callback',
            dest='end_datetime',
            callback=check_datetime,
            default=None,
            help='end datetime for interval [default: %default]'
        ),

        make_option ('-s', '--sleep',
            type='float',
            action='store',
            dest='sleep',
            default=0.025,
            help='seconds to sleep per tick [default: %default]'
        ),

        make_option ('-c', '--uri-client',
            type='string',
            action='store',
            dest='uri_clients',
            default='tcp://*:6667',
            help='uri for clients [default: %default]'
        ),

        make_option ('-t', '--io-threads',
            type='int',
            action='store',
            dest='sz_threads',
            default=1,
            help='size of the ZMQ thread pool to handle I/O operations \
                  [default: %default]'
        ),
    )
    
    ###########################################################################
    def handle (self, *args, **options):
    ###########################################################################

        logging.basicConfig (format='[%(asctime)s] %(levelname)s: %(message)s')

        srvlog_level = getattr(logging, options['srvlog_level'].upper(), None)
        if not isinstance(srvlog_level, int):
            raise CommandError('invalid level: %s' % options['srvlog_level'])
        srvlog = logging.getLogger ('srv')
        srvlog.setLevel (srvlog_level)

        msglog_level = getattr(logging, options['msglog_level'].upper(), None)
        if not isinstance(msglog_level, int):
            raise CommandError('invalid level: %s' % options['msglog_level'])
        msglog = logging.getLogger ('msg')
        msglog.setLevel (msglog_level)
        
        if options['tar_pair'] != None:
            srvlog.debug ('querying for pair "%s"' % options['tar_pair'])
            tar_quote, tar_base = options['tar_pair'].split ('/')
            from core.models import PAIR
            try: tar_pair = PAIR.objects.get (quote=tar_quote, base=tar_base)
            except Exception as e: raise CommandError (e)
        else:
            tar_pair = None

        srvlog.debug ('determining beg datetime')
        if options['beg_datetime'] != None:
            beg_datetime = options['beg_datetime']
        else:
            beg_datetime = datetime.min

        srvlog.debug ('determining end datetime')
        if options['end_datetime'] != None:
            end_datetime = options['end_datetime']
        else:
            end_datetime = datetime.max

        interval = {'beg':beg_datetime, 'end':end_datetime}

        if options['sleep'] != None: sleep = options['sleep']
        else: raise CommandError ('SLEEP not set')

        if options['uri_clients'] != None: uri_clients = options['uri_clients']
        else: raise CommandError ('URI_CLIENTS not set')

        if options['sz_threads'] != None: sz_threads = options['sz_threads']
        else: raise CommandError ('SZ_THREADS not set')

        try:
            self.server (
                interval, tar_pair, sleep, uri_clients, sz_threads
            )

        except KeyboardInterrupt:
            pass

        except Exception, ex:
            srvlog.exception (ex)

    ###########################################################################
    def server (self, interval, pair, sleep, uri_clients, sz_threads):
    ###########################################################################

        srvlog = logging.getLogger ('srv')
        srvlog.info ('starting server')

        srvlog.debug ('initiating ZMQ context')
        context = zmq.Context (sz_threads)

        srvlog.debug ('opening ZMQ PUB socket for clients')
        socket = context.socket (zmq.PUB)
        socket.bind (uri_clients)

        srvlog.info ('server started')
        try:
            self.main (socket, interval, pair, sleep)

        except KeyboardInterrupt:
            pass

        except Exception, ex:
            srvlog.exception (ex)

        finally:
            srvlog.info ('shutting server down')

            srvlog.debug ('closing clients\' socket')
            socket.close ()
            srvlog.debug ('terminating ZMQ context')
            context.term ()

            srvlog.info ('server shut down')

    ###########################################################################
    def main (self, socket, interval, pair = None, seconds = 0.025):
    ###########################################################################

        from core.models import TICK

        srvlog = logging.getLogger ('srv')
        msglog = logging.getLogger ('msg')

        beg_datetime = interval['beg']
        srvlog.info ('interval from: %s' % beg_datetime)
        end_datetime = interval['end'];
        srvlog.info ('interval till: %s' % end_datetime)

        if pair:
            ticks = TICK.objects.filter (pair=pair,
                datetime__gte=beg_datetime, datetime__lt=end_datetime
            )

        else:
            ticks = TICK.objects.filter (
                datetime__gte=beg_datetime, datetime__lt=end_datetime
            )

        for tick in ticks: ##TODO: Improve performance!

            message = '%s|%d|%0.6f|%0.6f' % (
                tick.pair, tick.unixstamp, tick.bid, tick.ask
            )

            socket.send (message)
            msglog.debug (message)

            time.sleep (seconds)

###############################################################################
###############################################################################
