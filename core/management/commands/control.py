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

    args = '<port>'
    help = 'Starts the foreign exchange server control service'

    def handle(self, *args, **options):

        ##
        ## TODO: Use proper option parsing!
        ##

        self.server ()
        
    def server (self, port = 6666):

        url_worker = "inproc://workers"
        url_client = "tcp://*:%s" % port

        context = zmq.Context (1)

        clients = context.socket (zmq.XREP)
        clients.bind (url_client)
        workers = context.socket (zmq.XREQ)
        workers.bind (url_worker)

        for id in range (3): ## number of workers!

            thread = threading.Thread (
                target=self.worker, args=(id, url_worker, context)
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

    def worker (self, id, url, context):

        socket = context.socket (zmq.REP)
        socket.connect (url)

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
