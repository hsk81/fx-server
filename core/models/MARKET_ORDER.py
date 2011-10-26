#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 29, 2011 8:28:01 PM$"

###############################################################################################
###############################################################################################

from core.models import *

###############################################################################################
###############################################################################################

class MARKET_ORDER (ORDER):

    """
    A MARKET_ORDER is used to create a spot trade.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'market orders'

    ###########################################################################################
    ###########################################################################################

    ## java.lang.Object clone()
    def clone (self):
        """
        Returns a exact copy of this MARKET_ORDER.
        """
        raise NotImplementedError

    ## MarketOrder getClose()
    def get_close (self):
        """
        ???
        """
        raise NotImplementedError

    ## double getRealizedPL()
    def get_realized_pl (self):
        """
        Returns the profit realized on this trade.
        """
        raise NotImplementedError

    ## int getTransactionLink()
    def get_transaction_link (self):
        """
        Returns the transaction number of any trade or order that is related to 
        this trade.
        """
        raise NotImplementedError

    ## double getUnrealizedPL(FXTick tick)
    def get_unrealized_pl (self, tick):
        """
        Returns the unrealized profit/loss held by this order based on the
        provided market rate.
        """
        raise NotImplementedError
    
    ###########################################################################################
    ###########################################################################################
    
    def __unicode__ (self):
        """
        Returns string representation for this MARKET_ORDER.
        """
        return "%s" % self.id

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
