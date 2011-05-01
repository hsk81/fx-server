#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 30, 2011 3:20:01 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *

###############################################################################
###############################################################################

## public class FXPair extends java.lang.Object implements java.lang.Cloneable
class PAIR (models.Model):

    """
    An PAIR object represents a pair of ISO currency symbols.
    """

    class Meta:

        app_label = 'core'

    quote = models.CharField (max_length = 3, blank = True)
    base = models.CharField (max_length = 3, blank = True)

    ## FXPair(java.lang.String base, java.lang.String quote)
    def __init__ (self, *args, **kwargs):
        """
        Creates a new FXPair object with the specified base and quote currency.
        """
        super (PAIR, self).__init__ (*args, **kwargs)

    ## java.lang.Object clone()
    def clone (self):
        """
        Returns a exact copy of this PAIR.
        """
        raise NotImplementedError

    ## int compareTo(FXPair fxpair)
    def compare_to (self, pair):
        """
        Performs a lexicographical comparison of two PAIR objects.
        """
        raise NotImplementedError

    ## boolean equals(java.lang.Object o)
    def equals (self, object):
        """
        Compares this PAIR to another PAIR.
        """
        raise NotImplementedError

    ## java.lang.String getBase()
    def get_base (self):
        """
        Returns the base currency.
        """
        return self.base
    
    ## FXPair getInverse()
    def get_inverse (self):
        """
        Returns a new PAIR object with the base and quote currency reversed.
        """
        return PAIR (quote = self.base, base = self.quote)

    ## java.lang.String getPair()
    def get_pair (self):
        """
        Returns the currency PAIR as a string.
        """
        return "%s/%s" % (self.quote, self.base)

    ## java.lang.String getQuote()
    def get_quote (self):
        """
        Returns the quote currency.
        """
        return self.quote
    
    ## int hashCode()
    def hash_code (self):
        """
        Return the hashcode of this PAIR.
        """
        raise NotImplementedError

    ## boolean isHalted()
    def is_halted (self):
        """
        Returns the trading status of this PAIR.
        """
        raise NotImplementedError

    ## void setBase(java.lang.String base)
    def set_base (self, base):
        """
        Sets the base currency.
        """
        self.base = base

    ## void setPair(java.lang.String pair)
    def set_pair (self, pair):
        """
        Sets the currency PAIR.
        """
        raise NotImplementedError

    ## void setQuote(java.lang.String quote)
    def set_quote (self, quote):
        """
        Sets the quote currency.
        """
        self.quote = quote

    def __unicode__ (self):
        """
        Returns string representation for this PAIR.
        """
        return self.get_pair ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
