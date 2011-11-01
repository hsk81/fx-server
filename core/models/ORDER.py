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

    def get_timestamp (self): self.update_date_unix
    def get_transaction_number (self): return self.id

###############################################################################################
###############################################################################################
