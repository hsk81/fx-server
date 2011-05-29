__author__ = "hsk81"
__date__ = "$May 15, 2011 2:07:29 AM$"

###############################################################################
###############################################################################

from django.core.management.base import *
from datetime import *

import threading
import zmq

###############################################################################
###############################################################################

class Command (BaseCommand):

    """
    The control command enables the control service for the FX server. Its main
    duty is to manage all the incoming control commands.
    """

    help = 'Starts the foreign exchange server control service'

    option_list = BaseCommand.option_list + (
        make_option ('--uri-client',
            type='string',
            action='store',
            dest='uri_client',
            default='tcp://*:6666',
            help='uri for clients [default: %default]'
        ),

        make_option ('--uri-worker',
            type='string',
            action='store',
            dest='uri_worker',
            default='inproc://workers:6667',
            help='uri for worker threads [default: %default]'
        ),
    )

    def handle(self, *args, **options):

        print args
        print options

        self.server (
            options['uri_worker'], options['uri_client']
        )
        
    def server (self, uri_worker, uri_client):

        context = zmq.Context (1)

        clients = context.socket (zmq.XREP)
        clients.bind (uri_client)
        workers = context.socket (zmq.XREQ)
        workers.bind (uri_worker)

        for id in range (3): ## number of workers!

            thread = threading.Thread (
                target=self.worker, args=(id, uri_worker, context)
            )

            thread.start ()

        try:

            zmq.device (zmq.QUEUE, clients, workers)

        except:

            pass ## enables ctrl-c!

        finally:

            clients.close ()
            workers.close ()
            context.term ()

    def worker (self, id, uri, context):

        socket = context.socket (zmq.REP)
        socket.connect (uri)

        while True:

            ##
            ## TODO: User proper logging instead of print >> self.stdout!
            ##

            request = socket.recv ()
            print >> self.stdout, '[%s] T%02d.REQ "%s"' % \
                (datetime.now (), id, request)

            response = self.process (*request.split('|'))            
            socket.send (response)
            print >> self.stdout, '[%s] T%02d.REP "%s"' % \
                (datetime.now (), id, response)

    def process (cls, method, *args):

        import core.models

        try:
            return getattr (core.models, cls).invoke (cls, method, *args)

        except Exception, ex:
            return 'EXCEPTION|%s' % ex

    process = staticmethod (process)

###############################################################################
###############################################################################
