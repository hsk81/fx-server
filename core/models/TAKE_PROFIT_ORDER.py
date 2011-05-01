#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 1, 2011 9:57:53 PM$"

###############################################################################
###############################################################################

from core.models import *

###############################################################################
###############################################################################

## public final class TakeProfitOrder extends Order implements 
## java.lang.Cloneable
class TAKE_PROFIT_ORDER (ORDER):

    """
    A TAKE_PROFIT_ORDER will close a MARKET_ORDER when the designated market
    rate is reached. Please note that setting any field other than the price
    field will have no effect.
    """

    class Meta:

        app_label = 'core'

    ##
    ## TODO!
    ##

if __name__ == "__main__":

    pass
