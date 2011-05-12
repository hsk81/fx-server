#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 8, 2011 12:16:49 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *
import time

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

    ###########################################################################
    ###########################################################################

    def __init__ (self, *args, **kwargs):

        super (TICK, self).__init__ (*args, **kwargs)

    ###########################################################################
    ###########################################################################

    datetime = models.DateTimeField (auto_now = True)

    ask = models.DecimalField (
        max_digits=9, decimal_places=6, default=0.000000
    )

    bid = models.DecimalField (
        max_digits=9, decimal_places=6, default=0.000000
    )

    pair = models.ForeignKey (PAIR)

    ###########################################################################
    ###########################################################################
    
    mean = property (lambda self: (self.ask + self.bid) / 2.0)
    inverse = property (lambda self: TICK (ask=self.bid, bid=self.ask))

    def get_unixstamp (self):

        return time.mktime (self.datetime_stamp.timetuple ())

    def set_unixstamp (self, value):

        self.datetime = datetime.fromtimestamp (value)

    unixstamp = property (get_unixstamp, set_unixstamp)
    
    def date (self):

        return self.datetime.strftime ('%Y %b %d')

    date.short_description = 'date'
    date.admin_order_field = 'datetime'

    def time (self):

        return self.datetime.strftime ('%H:%M:%S.%f')

    time.short_description = 'time'
    time.admin_order_field = 'datetime'

    ###########################################################################
    ###########################################################################
    
    def __unicode__ (self):

        return "%s/%s [%.6f,%.6f] @ %s" % (
            self.pair.quote, self.pair.base, self.ask, self.bid, self.datetime
        )
    
###############################################################################
###############################################################################

if __name__ == "__main__":

    pass

###############################################################################
###############################################################################
