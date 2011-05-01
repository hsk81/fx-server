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

    high_price_limit = models.DecimalField (
        max_digits = 15, decimal_places = 6, default = 0.000000)
    low_price_limit = models.DecimalField (
        max_digits = 15, decimal_places = 6, default = 0.000000)

    pair = models.ForeignKey (PAIR)
    
    _stop_loss_order = models.ForeignKey ('STOP_LOSS_ORDER')
    _take_profit_order = models.ForeignKey ('TAKE_PROFIT_ORDER')
    
    ## double getHighPriceLimit()
    def get_high_price_limit (self):
        """
        Returns the high price limit.
        """
        raise self.high_price_limit

    ## double getLowPriceLimit()
    def get_low_price_limit (self):
        """
        Returns the low price limit.
        """
        raise self.low_price_limit

    ## FXPair getPair()
    def get_pair (self):
        """
        Returns the PAIR.
        """
        raise self.pair

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
        return self._stop_loss_order

    ## TakeProfitOrder getTakeProfit()
    def get_take_profit (self):
        """
        Returns the TAKE_PROFIT_ORDER associated with this ORDER.
        """
        return self._take_profit_order

    ## long getTimestamp()
    def get_timestamp (self):
        """
        Returns the timestamp for this ORDER.
        """
        raise NotImplementedError

    ## int getTransactionNumber()
    def get_transaction_number (self):
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
        self.pair = pair

    ## void setStopLoss(StopLossOrder stoploss)
    def set_stop_loss (self, _stop_loss_order):
        """
        Sets the STOP_LOSS_ORDER for this ORDER.
        """
        self._stop_loss_order = _stop_loss_order

    ## void setTakeProfit(TakeProfitOrder takeprofit)
    def set_take_profit (self, _take_profit_order):
        """
        Sets the TAKE_PROFIT_ORDER for this ORDER.
        """
        self._take_profit_order = _take_profit_order

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
