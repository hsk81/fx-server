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
        max_digits = 15, decimal_places = 6, default = 0.000000)
    high_price_limit = models.DecimalField (
        max_digits = 15, decimal_places = 6, default = 0.000000)
    low_price_limit = models.DecimalField (
        max_digits = 15, decimal_places = 6, default = 0.000000)
    
    stop_loss = models.ForeignKey ('STOP_LOSS_ORDER')
    take_profit = models.ForeignKey ('TAKE_PROFIT_ORDER')

    ###########################################################################################
    ###########################################################################################

    def get_high_price_limit (self): return self.high_price_limit
    def get_low_price_limit (self): return self.low_price_limit
    def get_pair (self): return self.pair
    def get_price (self): return self.price
    def get_stop_loss (self): return self.stop_loss
    def get_take_profit (self): return self.take_profit
    def get_timestamp (self): return time.mktime (self.update_at.timetuple ())
    def get_transaction_number (self): return self.id
    def get_units (self): self.units
    def set_high_price_limit (self, limit): self.high_price_limit = limit
    def set_low_price_limit (self, limit): self.low_price_limit = limit
    def set_pair (self, pair): self.pair = pair
    def set_stop_loss (self, stop_loss): self.stop_loss = stop_loss
    def set_take_profit (self, take_profit): self.take_profit = take_profit
    def set_units (self, units): self.units = units

###############################################################################################
###############################################################################################
