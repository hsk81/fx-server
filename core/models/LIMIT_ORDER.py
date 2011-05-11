#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 8, 2011 12:00:09 PM$"

###############################################################################
###############################################################################

from core.models import *

###############################################################################
###############################################################################

## public final class LimitOrder extends EntryOrder implements Cloneable
class LIMIT_ORDER (ORDER):

    """
    A LIMIT_ORDER is a spot order that is executed when the target price is met.
    The STOP_LOSS_ORDER and TAKE_PROFIT_ORDER members will be carried over to
    the resulting trade.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'limit orders'

    ## java.lang.Object clone()
    def clone (self):
        """
        Returns a exact copy of this LIMIT_ORDER.
        """
        raise NotImplementedError
    
    ## java.lang.String toString()
    def __unicode__ (self):
        """
        ???
        """
        raise NotImplementedError
    
###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
