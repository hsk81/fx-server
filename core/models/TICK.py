#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 8, 2011 12:16:49 PM$"

###############################################################################################
###############################################################################################

from time import *
from core.models import *
from django.db import models

###############################################################################################
###############################################################################################

class TICK (models.Model):

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'ticks'

    ###########################################################################################
    ###########################################################################################

    def __init__ (self, *args, **kwargs):

        super (TICK, self).__init__ (*args, **kwargs)

    ###########################################################################################
    ###########################################################################################

    datetime = models.DateTimeField (db_index=True)
    ask = models.DecimalField (max_digits=9, decimal_places=6, default=0.000000)
    bid = models.DecimalField (max_digits=9, decimal_places=6, default=0.000000)
    pair = models.ForeignKey (PAIR)

    ###########################################################################################
    ###########################################################################################
    
    mean = property (lambda self: (self.ask + self.bid) / 2)
    inverse = property (lambda self: TICK (ask=self.bid, bid=self.ask))

    ###########################################################################################
    ###########################################################################################
    
    def get_unixstamp (self):

        return mktime (self.datetime.timetuple ())

    unixstamp = property (get_unixstamp)

    get_unixstamp.short_description = 'unixstamp'
    get_unixstamp.admin_order_field = 'datetime'
    
    def get_date (self):

        return self.datetime.strftime ('%Y-%m-%d')

    date = property (get_date)
    
    get_date.short_description = 'date'
    get_date.admin_order_field = 'datetime'

    def get_time (self):

        return self.datetime.strftime ('%H:%M:%S.%f')

    time = property (get_time)
    
    get_time.short_description = 'time'
    get_time.admin_order_field = 'datetime'

    ###########################################################################################
    ###########################################################################################
    
    def __unicode__ (self):

        return "[%.6f,%.6f] @ %d" % (self.bid, self.ask, self.unixstamp)
    
###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
