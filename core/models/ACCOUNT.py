__author__ = "hsk81"
__date__ = "$Apr 22, 2011 2:50:14 PM$"

###############################################################################################
###############################################################################################

from base.models import *
from core.models import *
from django.db import models
from django.core import serializers

import json

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

        ## TODO: Not thread safe ++> use transactions!
        ## TODO: either simulate (price) matching or set price to last tick!
        
        ## TODO: if mo.take_profit != null: mo.take_profit.save ()
        ## TODO: if mo.stop_loss != null: mo.stop_loss.save ()
        ## TODO: if mo.close != null: mo.close.save ()

        mo_fields = json.loads (mo)
        mo_pair = mo_fields['pair']
        pair = PAIR.objects.get (quote = mo_pair['quote'], base = mo_pair['base'])
        mo_fields['pair'] = pair.id
        mo_fields = json.dumps (mo_fields)
        
        market_orders = '[{"pk":%s,"model":"core.market_order","fields":%s}]' % (
            MARKET_ORDER.objects.count () + 1, mo_fields ## TODO: Not thread safe!
        )

        market_order = serializers.deserialize ('json', market_orders).next ()
        market_order.save () ## INFO: Means 'create-or-save'!
        market_orders = MARKET_ORDER.objects.filter (id = market_order.object.id)

        return serializers.serialize ('json', market_orders)

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
