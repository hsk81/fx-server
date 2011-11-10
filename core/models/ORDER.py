__author__ = "hsk81"
__date__ = "$Apr 29, 2011 8:28:01 PM$"

###############################################################################################
###############################################################################################

from base.models import *
from core.models import *
from django.db import models

###############################################################################################
###############################################################################################

class ORDER (BASE):

    class Meta:

        abstract = True
        app_label = 'core'
        verbose_name_plural = 'orders'

    ###########################################################################################
    ###########################################################################################

    units = models.IntegerField ()
    pair = models.ForeignKey (PAIR)

    price = models.DecimalField (
        max_digits = 15, decimal_places = 6)
    high_price_limit = models.DecimalField (
        max_digits = 15, decimal_places = 6, null = True, blank = True)
    low_price_limit = models.DecimalField (
        max_digits = 15, decimal_places = 6, null = True, blank = True)
    
    stop_loss = models.ForeignKey ('STOP_LOSS_ORDER', null = True, blank = True)
    take_profit = models.ForeignKey ('TAKE_PROFIT_ORDER', null = True, blank = True)

    transaction_number = models.IntegerField (null = True, blank = True)

    ###########################################################################################
    ###########################################################################################

    def __unicode__ (self):

        return "%s %s @ %0.6f" % (self.pair, self.units, self.price)

###############################################################################################
###############################################################################################
