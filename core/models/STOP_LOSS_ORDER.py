__author__ = "hsk81"
__date__ = "$May 1, 2011 9:57:42 PM$"

###############################################################################################
###############################################################################################

from core.models import *

###############################################################################################
###############################################################################################

class STOP_LOSS_ORDER (ORDER):

    """
    A STOP_LOSS_ORDER will close a MARKET_ORDER when the designated market rate
    is reached. Please note that setting any field other than the price field
    will have no effect.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'stop loss orders'

    ###########################################################################################
    ###########################################################################################

    ##
    ## TODO!
    ##

###############################################################################################
###############################################################################################
