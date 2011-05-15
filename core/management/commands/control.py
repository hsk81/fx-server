###############################################################################
###############################################################################

from django.core.management.base import *

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

        from core.models.TICK import TICK

        ts = TICK.objects.all ()
        print >> self.stdout, ts
