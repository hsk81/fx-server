###############################################################################
###############################################################################

from django.core.management.base import *

import time
import threading
import zmq

###############################################################################
###############################################################################

class Command (BaseCommand):

    """
    The control command enables the control service for the FX server. It's main
    duty is to manage all the incoming control commands.
    """

    args = '<port>'
    help = 'Starts the foreign exchange server control service'

    def handle(self, *args, **options):

        ##
        ## TODO: Implement access from clients using ZMQ!
        ##

        from core.models.TICK import TICK
        ts = TICK.objects.all ()
        print >> self.stdout, ts
