from django.db import models
from django.contrib import auth
from time import time

###############################################################################
###############################################################################

class STAMP (models.Model):
    """
    TODOC
    """
    insert_date = models.DateTimeField (auto_now_add = True)
    update_date = models.DateTimeField (auto_now = True)
    delete_date = models.DateTimeField (null = True)

    def __unicode__ (self):
        """
        Returns string representation for this stamp.
        """
        return "%s" % self.insert_date

###############################################################################
###############################################################################

class ADDRESS (models.Model):
    """
    TODOC
    """
    class Meta:

        verbose_name_plural = 'addresses'

    line1 = models.CharField (max_length = 256)
    line2 = models.CharField (max_length = 256, blank = True, default = '')
    zip = models.CharField (max_length = 256)
    city = models.CharField (max_length = 256)
    country = models.CharField (max_length = 256)

    def full_address (self, show_blank_line2 = False):
        """
        Returns string representation for this ADDRESS.
        """
        if show_blank_line2:
            return "%s\n%s\n%s %s\n%s" % (
                self.line1, self.line2, self.zip, self.city, self.country
            )
        else:
            return (self.line2 != "") and (
                "%s\n%s\n%s %s\n%s" % (
                    self.line1, self.line2, self.zip, self.city, self.country
                )
            ) or (
                "%s\n%s %s\n%s" % (
                    self.line1, self.zip, self.city, self.country
                )
            )

    def short_address (self, show_blank_line2 = False):
        """
        Returns string representation for this ADDRESS.
        """
        if show_blank_line2:
            return "%s\n%s\n%s %s" % (
                self.line1, self.line2, self.zip, self.city
            )
        else:
            return (self.line2 != "") and (
                "%s\n%s\n%s %s" % (self.line1, self.line2, self.zip, self.city)
            ) or (
                "%s\n%s %s" % (self.line1, self.zip, self.city)
            )


    def __unicode__ (self):
        """
        Returns string representation for this ADDRESS.
        """
        return self.short_address ()

###############################################################################
###############################################################################

## public final class User extends java.lang.Object
class USER (auth.models.User):
    """
    Provides access to USER information.
    """
    address = models.ForeignKey (ADDRESS)
    phone = models.CharField (max_length = 256)
    profile = models.CharField (max_length = 256, blank = True, default = '')

    ## java.util.Vector getAccounts()
    def get_accounts (self):
        """
        Returns a vector of ACCOUNTs owned by this USER.
        """
        return self.accounts.all ()

    ## ACCOUNT getAccountWithId(int accountId)
    def get_account_with_id (self, account_id):
        """
        Returns the ACCOUNT owned by this USER with the given account_id.
        """
        return self.accounts.get (id = account_id)

    ## java.lang.String getAddress()
    def get_address (self):
        """
        Returns the USERs ADDRESS.
        """
        return "%s" % self.adress

    ## long getCreateDate()
    def get_create_date (self):
        """
        Returns the date this USER was created as a unix timestamp.
        """
        return time.mktime (self.date_joined.timetuple ())

    ## java.lang.String getEmail()
    def get_email (self):
        """
        Returns this USERs email address.
        """
        return "%s" % self.email

    ## java.lang.String getName()
    def get_name (self):
        """
        Returns this USERs full name.
        """
        return "%s, %s" % (self.last_name, self.first_name)

    ## java.lang.String getPassword()
    def get_password (self):
        """
        Returns the login password for this USER.
        """
        return "%s" % self.password

    ## java.lang.String getProfile()
    def get_profile (self):
        """
        Returns the profile string for this USER.
        """
        return "%s" % self.profile

    ## java.lang.String getTelephone()
    def get_telephone (self):
        """
        Returns this USERs telephone number.
        """
        return "%s" % self.phone

    ## int getUserId()
    def get_user_id (self):
        """
        Returns this USERs unique id number.
        """
        return self.pk

    ## java.lang.String getUserName()
    def get_user_name (self):
        """
        Returns the login username for this USER.
        """
        return "%s" % self.username

    ## void setProfile(java.lang.String newprofile)
    def set_profile (self, new_profile):
        """
        Sends a profile string to be saved on the server and associated with
        this USER.
        """
        self.profile = new_profile

    ## java.lang.String toString()
    def __unicode__ (self):
        """
        Returns string representation for this USER.
        """
        return "%s, %s" % (self.last_name, self.first_name)

###############################################################################
###############################################################################

class CURRENCY (models.Model):
    """
    TODOC
    """
    code = models.CharField (max_length = 3)
    name = models.CharField (max_length = 256)

    def __unicode__ (self):
        """
        Returns string representation for this CURRENCY.
        """
        return "%s" % self.code

###############################################################################
###############################################################################

## public final class Account extends java.lang.Object
class ACCOUNT (models.Model):
    """
    An ACCOUNT object represents an existing trading account. ACCOUNTs cannot
    be created through this API. ACCOUNTs are identified by a unique integer id
    (account_id). Current open trades, ORDERs and TRANSACTIONs are maintained
    and kept up-to-date within the object.
    """
    stamp = models.ForeignKey (STAMP)
    user = models.ForeignKey (USER, related_name = 'accounts')
    name = models.CharField (max_length = 256)
    home_currency = models.ForeignKey (CURRENCY)
    profile = models.CharField (max_length = 256, blank = True, default = '')

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
        return self.pk

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
        raise NotImplementedError

    ## long getCreateDate()
    def get_create_date (self):
        """
        Returns the creation date for this account expressed as a unix
        timestamp.
        """
        return time.mktime (self.stame.insert_date.timetuple ())

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
        Returns the Vector of LIMIT_ORDERs held by this account, querying the
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
        Returns the Vector of MARKET_ORDERs currently held by this account,
        querying the server if neccessary.
        """
        raise NotImplementedError
    
    ## MARKET_ORDER getTradeWithId(int transactionNumber)
    def get_trade_with_id (self, transaction_number):
        """
        Returns the MARKET_ORDER with the given transaction number.
        """
        raise NotImplementedError

    ## java.util.Vector getTransactions()
    def get_transactions (self):
        """
        Returns a Vector of TRANSACTIONs that have recently occured on this
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
        
    ## java.lang.String toString()
    def __unicode__ (self):
        """
        Returns string representation for this ACCOUNT.
        """
        return "%s" % self.name

###############################################################################
###############################################################################
