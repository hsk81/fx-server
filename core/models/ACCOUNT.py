#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 22, 2011 2:50:14 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *

###############################################################################
###############################################################################

## public final class Account extends Object
class ACCOUNT (models.Model):

    """
    An ACCOUNT object represents an existing trading account. ACCOUNTs cannot
    be created through this API. ACCOUNTs are identified by a unique integer id
    (account_id). Current open trades, ORDERs and TRANSACTIONs are maintained
    and kept up-to-date within the object.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'accounts'

    stamp = models.ForeignKey (STAMP)
    user = models.ForeignKey (USER, related_name = 'accounts')
    name = models.CharField (max_length = 256)
    profile = models.CharField (max_length = 256, blank = True, default = '')
    home_currency = models.CharField (max_length = 3)

    balance = models.DecimalField (
        max_digits = 15, decimal_places = 6, default = 0.000000
    )

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

    ## int getAccountId()
    def get_account_id (self):
        """
        Returns the unique id number associated with this ACCOUNT.
        """
        return self.id

    ## java.lang.String getAccountName()
    def get_account_name (self):
        """
        Returns the account name.
        """
        return "%s" % self.name

    ## double getBalance()
    def get_balance (self):
        """
        Returns the most up-to-date account balance, querying the server if
        neccessary.
        """
        return self.balance

    ## long getCreateDate()
    def get_create_date (self):
        """
        Returns the creation date for this account expressed as a unix
        timestamp.
        """
        return time.mktime (self.stamp.insert_date.timetuple ())

    ## FXEventManager getEventManager()
    def get_event_manager (self):
        """
        Gets the event manager for this account
        """
        raise NotImplementedError

    ## java.lang.String getHomeCurrency()
    def get_home_currency (self):
        """
        Returns the home currency for this ACCOUNT.
        """
        return "%" % self.home_currency

    ## double getMarginAvailable()
    def get_margin_available (self):
        """
        Returns the most up-to-date margin available value, querying the
        server if neccessary.
        """
        raise NotImplementedError

    ## double getMarginCallRate()
    def get_margin_call_rate (self):
        """
        Returns the margin call rate.
        """
        raise NotImplementedError

    ## double getMarginRate()
    def get_margin_rate (self):
        """
        Returns the margin rate.
        """
        raise NotImplementedError

    ## double getMarginUsed()
    def get_margin_used (self):
        """
        Returns the most up-to-date margin used value, querying the server if
        neccessary.
        """
        raise NotImplementedError

    ## java.util.Vector getOrders()
    def get_orders (self):
        """
        Returns the vector of LIMIT_ORDERs held by this account, querying the
        server if neccessary.
        """
        raise NotImplementedError

    ## LIMIT_ORDER getOrderWithId(int transactionNumber)
    def get_order_with_id (self, transaction_number):
        """
        Returns the LIMIT_ORDER with the given transaction number.
        """
        raise NotImplementedError

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
        Returns the most up-to-date values of all trades held by this account
        based in home currency, querying the server if neccessary.
        """
        raise NotImplementedError

    ## java.lang.String getProfile()
    def get_profile (self):
        """
        Returns the profile string for this ACCOUNT.
        """
        return "%s" % self.profile

    ## double getRealizedPL()
    def get_realized_pl (self):
        """
        Returns the most up-to-date realized profit/loss value, querying the
        server if neccessary.
        """
        raise NotImplementedError

    ## java.util.Vector getTrades()
    def get_trades (self):
        """
        Returns the vector of MARKET_ORDERs currently held by this account,
        querying the server if neccessary.
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

    ## java.util.Vector getTransactions()
    def get_transactions (self):
        """
        Returns a vector of TRANSACTIONs that have recently occured on this
        account, querying the server if neccessary.
        """
        raise NotImplementedError

    ## TRANSACTION getTransactionWithId(int transactionNumber)
    def get_transaction_with_id (self, transaction_number):
        """
        Returns the TRANSACTION with the given transaction number.
        """
        raise NotImplementedError

    ## double getUnrealizedPL()
    def get_unrealized_pl (self):
        """
        Returns the most up-to-date unrealized profit/loss value, querying the
        server if neccessary.
        """
        raise NotImplementedError

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

    ## void setProfile(java.lang.String newprofile)
    def set_profile (self, new_profile):
        """
        Sends a profile string to be saved on the server and associated with
        this ACCOUNT.
        """
        self.profile = new_profile

    ###########################################################################
    ###########################################################################
    
    ## java.lang.String toString()
    def __unicode__ (self):
        
        return "%s" % self.name

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
