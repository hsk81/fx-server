#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 22, 2011 2:50:14 PM$"

###############################################################################################
###############################################################################################

from base.models import *
from core.models import *
from django.db import models

###############################################################################################
###############################################################################################

class ACCOUNT (BASE):

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'accounts'

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
        """
        Returns the most up-to-date margin available value, querying the server if neccessary.
        """
        raise NotImplementedError

    def get_margin_used (self):
        """
        Returns the most up-to-date margin used value, querying the server if neccessary.
        """
        raise NotImplementedError

    ###########################################################################################

    ## void close(LIMIT_ORDER lo)
    def close_limit_order (self, lo):
        """
        Closes the specified LIMIT_ORDER.
        """
        raise NotImplementedError

    ## void close(MARKET_ORDER mo)
    def close_market_order (self, mo):
        """
        Closes the specified MARKET_ORDER.
        """
        raise NotImplementedError

    ## void close(java.lang.String position)
    def close_position (self, position):
        """
        ???
        """
        raise NotImplementedError

    ###########################################################################################
    
    ## void execute(LIMIT_ORDER lo)
    def execute_limit_order (self, lo):
        """
        Executes the specified LIMIT_ORDER.
        """
        raise NotImplementedError

    ## void execute(MARKET_ORDER mo)
    def execute_market_order (self, mo):
        """
        Executes the specified MARKET_ORDER.
        """
        raise NotImplementedError

    ###########################################################################################

    ## void modify(LIMIT_ORDER lo)
    def modify_limit_order (self, lo):
        """
        Modifies the specified LIMIT_ORDER.
        """
        raise NotImplementedError

    ## void modify(MARKET_ORDER mo)
    def modify_market_order (self, mo):
        """
        Modifies the specified MARKET_ORDER.
        """
        raise NotImplementedError

    ###########################################################################################

    ## java.util.Vector getOrders()
    def get_orders (self):
        """
        Returns the vector of LIMIT_ORDERs held by this account, querying the server if
        neccessary.
        """
        raise NotImplementedError

    ## LIMIT_ORDER getOrderWithId(int transactionNumber)
    def get_order_with_id (self, transaction_number):
        """
        Returns the LIMIT_ORDER with the given transaction number.
        """
        raise NotImplementedError

    ###########################################################################################

    ## Position getPosition(FX_PAIR pair)
    def get_position (self, pair):
        """
        Get the currently open market position for a given pair.
        """
        raise NotImplementedError

    ## java.util.Vector getPositions()
    def get_positions (self):
        """
        Get all the currently open market positions.
        """
        raise NotImplementedError

    ## double getPositionValue()
    def get_position_value (self):
        """
        Returns the most up-to-date values of all trades held by this account based in home
        currency, querying the server if neccessary.
        """
        raise NotImplementedError

    ###########################################################################################

    ## double getRealizedPL()
    def get_realized_pl (self):
        """
        Returns the most up-to-date realized profit/loss value, querying the
        server if neccessary.
        """
        raise NotImplementedError

    ## double getUnrealizedPL()
    def get_unrealized_pl (self):
        """
        Returns the most up-to-date unrealized profit/loss value, querying the server if
        neccessary.
        """
        raise NotImplementedError

    ###########################################################################################

    ## java.util.Vector getTrades()
    def get_trades (self):
        """
        Returns the vector of MARKET_ORDERs currently held by this account, querying the server
        if neccessary.
        """
        return MARKET_ORDER.objects.filter (account__id = self.id)

    ## MARKET_ORDER getTradeWithId(int transactionNumber)
    def get_trade_with_id (self, transaction_number):
        """
        Returns the MARKET_ORDER with the given transaction number.
        """
        return MARKET_ORDER.objects.get (
            account__id = self.id,
            transaction_number = transaction_number
        )

    ###########################################################################################

    ## java.util.Vector getTransactions()
    def get_transactions (self):
        """
        Returns a vector of TRANSACTIONs that have recently occured on this account, querying
        the server if neccessary.
        """
        raise NotImplementedError

    ## TRANSACTION getTransactionWithId(int transactionNumber)
    def get_transaction_with_id (self, transaction_number):
        """
        Returns the TRANSACTION with the given transaction number.
        """
        raise NotImplementedError

    ###########################################################################################
    ###########################################################################################
    
    def __unicode__ (self):
        
        return "%s" % self.name

###############################################################################################
###############################################################################################

class WRAP:

    def invoke (cls, method, *args):

        return getattr (WRAP, method)(cls, method, *args)

    invoke = staticmethod (invoke)

    def get_info (cls, method, session_token, account_id):

        session = SESSION.objects.get (
            token = session_token, stamp__delete_date__isnull = True
        )

        account = session.user.accounts.get (
            id = account_id
        )

        return '%s|%s|%s|%s' % (cls, method, session_token, '|'.join (
            map (lambda value: value and str (value) or str (None), account.info)
        ))

    get_info = staticmethod (get_info)
    
###############################################################################################
###############################################################################################

ACCOUNT.invoke = staticmethod (WRAP.invoke)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
