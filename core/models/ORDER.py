#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 29, 2011 8:28:01 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *

###############################################################################
###############################################################################

## public abstract class Order extends java.lang.Object
class ORDER (models.Model):

    """
    ORDER is an abstract base class encapsulating the basic components of an
    forex order. Note that a sell order is indicated by specifying negative
    units.
    """

    class Meta:

        app_label = 'core'
        abstract = True

    ## double getHighPriceLimit()
    def get_high_price_limit (self):
        """
        Returns the high price limit.
        """
        raise NotImplementedError

    ## double getLowPriceLimit()
    def get_low_price_limit (self):
        """
        Returns the low price limit.
        """
        raise NotImplementedError

    ## FXPair getPair()
    def get_pair (self):
        """
        Returns the PAIR.
        """
        raise NotImplementedError

    ## double getPrice()
    def get_price (self):
        """
        Returns the ORDER price.
        """
        raise NotImplementedError

    ## StopLossOrder getStopLoss()
    def get_stop_loss (self):
        """
        Returns the STOP_LOSS_ORDER associated with this ORDER.
        """
        raise NotImplementedError

    ## TakeProfitOrder getTakeProfit()
    def get_take_profit (self):
        """
        Returns the TAKE_PROFIT_ORDER associated with this ORDER.
        """
        raise NotImplementedError

    ## long getTimestamp()
    def get_timestamp (self):
        """
        Returns the timestamp for this ORDER.
        """
        raise NotImplementedError

    ## int getTransactionNumber()
    def get_transaction_numbe (self):
        """
        Returns the transaction number.
        """
        raise NotImplementedError

    ## long getUnits()
    def get_units (self):
        """
        Returns the units field.
        """
        raise NotImplementedError

    ## void setHighPriceLimit(double limit)
    def set_high_price_limit (self, limit):
        """
        Sets the highest price that this order will trigger at.
        """
        raise NotImplementedError

    ## void setLowPriceLimit(double limit)
    def set_low_price_limit (self, limit):
        """
        Sets the lowest price that this order will trigger at.
        """
        raise NotImplementedError

    ## void setPair(FXPair pair)
    def set_pair (self, pair):
        """
        Sets the currency PAIR for this ORDER.
        """
        raise NotImplementedError

    ## void setStopLoss(StopLossOrder stoploss)
    def set_stop_loss (self, stop_loss):
        """
        Sets the STOP_LOSS_ORDER for this ORDER.
        """
        raise NotImplementedError

    ## void setTakeProfit(TakeProfitOrder takeprofit)
    def set_take_profit (self, take_profit):
        """
        Sets the TAKE_PROFIT_ORDER for this ORDER.
        """
        raise NotImplementedError

    ## void setUnits(long units)
    def set_units (self, units):
        """
        Sets the units.
        """
        raise NotImplementedError


###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
