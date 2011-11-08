__author__ = "hsk81"
__date__ = "$Apr 22, 2011 2:50:14 PM$"

###############################################################################################
###############################################################################################

import json

from base.models import *
from core.models import *
from django.db import models

###############################################################################################
###############################################################################################

class ACCOUNT (BASE):

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'accounts'

    ###########################################################################################
    ###########################################################################################

    user = models.ForeignKey (USER, related_name = 'accounts')
    name = models.CharField (max_length = 256)
    profile = models.CharField (max_length = 256, blank = True, default = '')
    home_currency = models.CharField (max_length = 3)

    balance = models.DecimalField (max_digits = 15, decimal_places = 6, default = 0.000000)
    margin_call_rate = models.DecimalField (max_digits = 3, decimal_places = 2, default = 0.50)
    margin_rate = models.DecimalField (max_digits = 3, decimal_places = 2, default = 0.10)

    ###########################################################################################
    ###########################################################################################
    
    @property
    def info (self):

        return [
            self.id,
            self.name,
            self.insert_date_unix,
            self.home_currency,
            self.profile,
            self.margin_call_rate,
            self.margin_rate
        ]

    ###########################################################################################
    ###########################################################################################

    def get_margin_available (self):
        raise NotImplementedError

    def get_margin_used (self):
        raise NotImplementedError

    ###########################################################################################

    def close_limit_order (self, lo):
        raise NotImplementedError

    def close_market_order (self, mo):
        raise NotImplementedError

    def close_position (self, position):
        raise NotImplementedError

    ###########################################################################################
    
    def execute_limit_order (self, lo):
        
        raise NotImplementedError

    def execute_market_order (self, mo):

        return json.loads (mo)

    ###########################################################################################

    def modify_limit_order (self, lo):
        raise NotImplementedError

    def modify_market_order (self, mo):
        raise NotImplementedError

    ###########################################################################################

    def get_orders (self):
        raise NotImplementedError

    def get_order_with_id (self, transaction_number):
        raise NotImplementedError

    ###########################################################################################

    def get_position (self, pair):
        raise NotImplementedError

    def get_positions (self):
        raise NotImplementedError

    def get_position_value (self):
        raise NotImplementedError

    ###########################################################################################

    def get_realized_pl (self):
        raise NotImplementedError

    def get_unrealized_pl (self):
        raise NotImplementedError

    ###########################################################################################

    def get_trades (self):
        
        return MARKET_ORDER.objects.filter (account__id = self.id)

    def get_trade_with_id (self, transaction_number):

        return MARKET_ORDER.objects.get (
            account__id = self.id, transaction_number = transaction_number
        )

    ###########################################################################################

    def get_transactions (self):
        raise NotImplementedError

    def get_transaction_with_id (self, transaction_number):
        raise NotImplementedError

    ###########################################################################################
    ###########################################################################################
    
    def __unicode__ (self):
        
        return "%s" % self.name

###############################################################################################
###############################################################################################

class WRAP:

    def invoke (cls, method, *args):

        return getattr (WRAP, method) (*args)

    invoke = staticmethod (invoke)

    def execute_market_order (session_token, account_id, market_order):

        session = SESSION.objects.get (token = session_token, delete_date__isnull = True)
        account = session.user.accounts.get (id = account_id)

        return '%s' % account.execute_market_order (market_order)

    execute_market_order = staticmethod (execute_market_order)

    def get_info (session_token, account_id):

        session = SESSION.objects.get (token = session_token, delete_date__isnull = True)
        account = session.user.accounts.get (id = account_id)

        return '|'.join (map (
            lambda value: value and str (value) or str (None), account.info
        ))

    get_info = staticmethod (get_info)
    
###############################################################################################
###############################################################################################

ACCOUNT.invoke = staticmethod (WRAP.invoke)

###############################################################################################
###############################################################################################
