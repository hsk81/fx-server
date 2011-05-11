#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 8, 2011 12:16:49 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *

###############################################################################
###############################################################################

## public final class FXTick extends Object implements Cloneable
class TICK (models.Model):

    """
    A TICK object represents a single forex spot price.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'ticks'

    timestamp = models.DateTimeField (auto_now = True)

    ask = models.DecimalField (
        max_digits=9, decimal_places=6, default=0.000000
    )

    bid = models.DecimalField (
        max_digits=9, decimal_places=6, default=0.000000
    )

    pair = models.ForeignKey (PAIR)

    ## FXTick(long timestamp, double bid, double ask) 
    def __init__ (self, *args, **kwargs):

        super (TICK, self).__init__ (*args, **kwargs)

    ## java.lang.Object clone()
    def clone (self):
        """
        Returns a exact copy of this TICK.
        """
        return TICK (timestamp=self.timestamp, bid=self.bid, ask=self.ask)
    
    ## boolean equals(java.lang.Object o)
    def equals (self, tick):
        """
        Compares two TICK objects.
        """
        raise NotImplementedError

    ## double getAsk()
    def get_ask (self):
        """
        Returns the ask price.
        """
        return self.ask

    ## double getBid()
    def get_bid (self):
        """
        Returns the bid price.
        """
        return self.bid

    ## FXTick getInverse()
    def get_inverse (self):
        """
        Return a new TICK which is the inverse of this TICK.
        """
        raise NotImplementedError

    ## double getMean()
    def get_mean (self):
        """
        ???
        """
        raise NotImplementedError

    ## long getTimestamp()
    def get_timestamp (self):
        """
        Returns the unix timestamp for this TICK.
        """
        time.mktime (self.timestamp.timetuple ())

    ## int hashCode()
    def hash_code (self):
        """
        Return the hashcode of this pair.
        """
        raise NotImplementedError

    ## void setAsk(double ask)
    def set_ask (self, ask):
        """
        Sets the ask price.
        """
        self.ask = ask

    ## void setBid(double bid)
    def set_bid (self, bid):
        """
        Sets the bid price.
        """
        self.bid = bid
        
    ## void setTimestamp(long timestamp)
    def set_timestamp (self, timestamp):
        """
        Sets the timestamp.
        """
        self.timestamp = datetime.fromtimestamp (timestamp)

    ## java.lang.String toString()
    def __unicode__ (self):
        """
        ???
        """
        return "%s: [%.6f,%.6f] for %s" % (
            self.timestamp, self.ask, self.bid, self.pair
        )
    
###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
