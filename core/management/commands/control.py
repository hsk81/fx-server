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

        for id in range (5):

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
            print >> self.stdout, '[%s] T%02d.REQ "%s"' % (datetime.now (), id, request)

            cls, method, args = request.split('|')
            response = self.process (cls, method, args)
            
            socket.send (response)
            print >> self.stdout, '[%s] T%02d.REP "%s"' % (datetime.now (), id, response)

    def process (self, cls, method, args):

        from core.models import PAIR

        ##
        ## TODO: Generalize (reflection) to get instances and methods! Further
        ##       think about message format efficiency!
        ##

        if cls == 'PAIR':
            if method == 'get_halted':
                try:
                    q2b = args.split ('/')
                    pair = PAIR.objects.get (quote = q2b[0], base = q2b[1])

                    return '%s|%s|%s|%s' % (cls,method,args,pair.get_halted ())
                except Exception, ex:
                    return 'EXCEPTION|%s' % ex
            else:
                return 'EXCEPTION|no method'
        else:
            return 'EXCEPTION|no class'

###############################################################################
###############################################################################
