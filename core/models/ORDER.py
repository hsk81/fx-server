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

    stamp = models.ForeignKey (STAMP)

    units = models.IntegerField ()
    pair = models.ForeignKey (PAIR)

    price = models.DecimalField (
        max_digits = 15, decimal_places = 6, default = 0.000000)
    high_price_limit = models.DecimalField (
        max_digits = 15, decimal_places = 6, default = 0.000000)
    low_price_limit = models.DecimalField (
        max_digits = 15, decimal_places = 6, default = 0.000000)
    
    stop_loss = models.ForeignKey ('STOP_LOSS_ORDER')
    take_profit = models.ForeignKey ('TAKE_PROFIT_ORDER')

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
        raise self.price

    ## StopLossOrder getStopLoss()
    def get_stop_loss (self):
        """
        Returns the STOP_LOSS_ORDER associated with this ORDER.
        """
        return self.stop_loss

    ## TakeProfitOrder getTakeProfit()
    def get_take_profit (self):
        """
        Returns the TAKE_PROFIT_ORDER associated with this ORDER.
        """
        return self.take_profit

    ## long getTimestamp()
    def get_timestamp (self):
        """
        Returns the timestamp for this ORDER.
        """
        return time.mktime (self.stamp.update_date.timetuple ())

    ## int getTransactionNumber()
    def get_transaction_number (self):
        """
        Returns the transaction number.
        """
        return self.id

    ## long getUnits()
    def get_units (self):
        """
        Returns the units field.
        """
        self.units

    ## void setHighPriceLimit(double limit)
    def set_high_price_limit (self, limit):
        """
        Sets the highest price that this order will trigger at.
        """
        self.high_price_limit = limit

    ## void setLowPriceLimit(double limit)
    def set_low_price_limit (self, limit):
        """
        Sets the lowest price that this order will trigger at.
        """
        self.low_price_limit = limit

    ## void setPair(FXPair pair)
    def set_pair (self, pair):
        """
        Sets the currency PAIR for this ORDER.
        """
        self.pair = pair

    ## void setStopLoss(StopLossOrder stoploss)
    def set_stop_loss (self, stop_loss):
        """
        Sets the STOP_LOSS_ORDER for this ORDER.
        """
        self.stop_loss = stop_loss

    ## void setTakeProfit(TakeProfitOrder takeprofit)
    def set_take_profit (self, take_profit):
        """
        Sets the TAKE_PROFIT_ORDER for this ORDER.
        """
        self.take_profit = take_profit

    ## void setUnits(long units)
    def set_units (self, units):
        """
        Sets the units.
        """
        self.units = units

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
