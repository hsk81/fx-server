__author__ = "hsk81"
__date__ = "$May 15, 2011 2:07:29 AM$"

###############################################################################
###############################################################################

from django.core.management.base import *
from datetime import *

import threading
import logging
import zmq

###############################################################################
###############################################################################

class Command (BaseCommand):
    
    ###########################################################################
    ###########################################################################

    help = 'Runs the foreign exchange server\'s main service'

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

        make_option ('-c', '--uri-client',
            type='string',
            action='store',
            dest='uri_clients',
            default='tcp://*:6666',
            help='uri for clients [default: %default]'
        ),

        make_option ('-w', '--uri-worker',
            type='string',
            action='store',
            dest='uri_workers',
            default='inproc://workers',
            help='uri for worker threads [default: %default]'
        ),

        make_option ('-n', '--workers',
            type='int',
            action='store',
            dest='sz_workers',
            default=3,
            help='number of worker threads [default: %default]'
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
    def handle(self, *args, **options):
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

        try:
            self.server (
                options['uri_clients'],
                options['uri_workers'],
                options['sz_workers'],
                options['sz_threads']
            )

        except KeyboardInterrupt:
            pass

        except Exception, ex:
            srvlog.exception (ex)
            
    ###########################################################################
    def server (self, uri_clients, uri_workers, sz_workers, sz_threads):
    ###########################################################################

        srvlog = logging.getLogger ('srv')
        srvlog.info ('starting server')

        srvlog.debug ('initiating ZMQ context')
        context = zmq.Context (sz_threads)

        srvlog.debug ('opening ZMQ XREP socket for clients')
        clients = context.socket (zmq.XREP)
        clients.bind (uri_clients)

        srvlog.debug ('opening ZMQ XREQ socket for workers')
        workers = context.socket (zmq.XREQ)
        workers.bind (uri_workers)

        srvlog.debug ('starting worker threads')
        for id in range (sz_workers): ## number of workers!

            srvlog.debug ('initiating worker thread T%02d' % id)
            thread = threading.Thread (
                target=self.worker, args=(id, uri_workers, context)
            )

            srvlog.debug ('starting worker thread T%02d' % id)
            thread.start ()

        srvlog.info ('server started')
        try:
            
            srvlog.debug ('initiating ZMQ QUEUE device')
            zmq.device (zmq.QUEUE, clients, workers)

        except: ## enables ctrl-c!

            pass

        finally:

            srvlog.info ('shutting server down')

            srvlog.debug ('closing clients\' socket')
            clients.close ()
            srvlog.debug ('closing workers\' socket')
            workers.close ()

            srvlog.debug ('terminating ZMQ context')
            context.term ()

            srvlog.info ('server shut down')

    ###########################################################################
    def worker (self, id, uri, context):
    ###########################################################################

        srvlog = logging.getLogger ('srv')
        msglog = logging.getLogger ('msg')

        srvlog.info ('T%02d - worker thread started' % id)

        srvlog.debug ('T%02d - initiating ZMQ REP socket' % id)
        socket = context.socket (zmq.REP)
        srvlog.debug ('T%02d - connecting to %s' % (id, uri))
        socket.connect (uri)
        
        while True:

            try:
                request = socket.recv ()
                msglog.debug ('T%02d - REQ "%s"' % (id, request))

                response = self.process (*request.split ('|'))
                msglog.debug ('T%02d - REP "%s"' % (id, response))

                socket.send (response)

            except zmq.ZMQError, ex:
                srvlog.debug ('T%02d - %s' % (id, ex))
                break

            except Exception, ex:
                srvlog.exception ('T%02d - %s' % (id, ex))
                break

        srvlog.info ('T%02d - worker thread stopped' % id)

    ###########################################################################
    def process (self, cls, method, *args):
    ###########################################################################

        import core.models
        try:

            return getattr (core.models, cls).invoke (cls, method, *args)

        except Exception, ex:

            logging.getLogger ('srv').exception (ex)
            return 'EXCEPTION|%s' % ex

###############################################################################
###############################################################################
