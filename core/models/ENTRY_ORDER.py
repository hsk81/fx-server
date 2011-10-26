#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 8, 2011 11:52:15 AM$"

###############################################################################################
###############################################################################################

from core.models import *

###############################################################################################
###############################################################################################

class ENTRY_ORDER (ORDER):

    """
    ENTRY_ORDER is an abstract base class extending class ORDER to include
    expiry and desired execution price information.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'entry orders'
        abstract = True

    ###########################################################################################
    ###########################################################################################

    ## long getExpiry()
    def get_expiry (self):
        """
        Returns this order's expiry date expressed as a unix timestamp.
        """
        raise NotImplementedException

    ## void setExpiry(long expiry)
    def set_expiry (self, expiry):
        """
        Sets the expiry date for this order.
        """
        raise NotImplementedException

    ## void setPrice(double price)
    def set_price (self, price):
        """
        Sets the desired execution price for this order.
        """
        raise NotImplementedException

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
