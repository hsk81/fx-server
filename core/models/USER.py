#! /usr/bin/python

__author__="hsk81"
__date__ ="$Apr 22, 2011 2:50:14 PM$"

###############################################################################
###############################################################################

from django.db import models
from django.contrib import auth
from time import time
from core.models import *

###############################################################################
###############################################################################

## public final class User extends java.lang.Object
class USER (auth.models.User):

    """
    Provides access to USER information.
    """
    
    class Meta:

        app_label = 'core'

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

if __name__ == "__main__":

    pass
