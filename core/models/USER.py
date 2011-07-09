#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 22, 2011 2:50:14 PM$"

###############################################################################
###############################################################################

from django.db import models
from django.contrib import auth
from time import time
from core.models import *

###############################################################################
###############################################################################

class USER (auth.models.User):

    """
    Provides access to USER information.
    """
    
    class Meta:

        app_label = 'core'
        verbose_name_plural = 'users'

    address = models.ForeignKey (ADDRESS)
    phone = models.CharField (max_length = 256)
    profile = models.CharField (max_length = 256, blank = True, default = '')

    def get_accounts (self):
        """
        Returns a vector of ACCOUNTs owned by this USER.
        """
        return self.accounts.all ()

    def get_account_with_id (self, account_id):
        """
        Returns the ACCOUNT owned by this USER with the given account_id.
        """
        return self.accounts.get (id = account_id)

    def get_address (self):
        """
        Returns the USERs ADDRESS.
        """
        return "%s" % self.adress

    def get_create_date (self):
        """
        Returns the date this USER was created as a unix timestamp.
        """
        return time.mktime (self.date_joined.timetuple ())

    def get_email (self):
        """
        Returns this USERs email address.
        """
        return "%s" % self.email

    def get_name (self):
        """
        Returns this USERs full name.
        """
        return "%s, %s" % (self.last_name, self.first_name)

    def get_password (self):
        """
        Returns the login password for this USER.
        """
        return "%s" % self.password

    def get_profile (self):
        """
        Returns the profile string for this USER.
        """
        return "%s" % self.profile

    def get_telephone (self):
        """
        Returns this USERs telephone number.
        """
        return "%s" % self.phone

    def get_user_id (self):
        """
        Returns this USERs unique id number.
        """
        return self.id

    def get_username (self):
        """
        Returns the login username for this USER.
        """
        return "%s" % self.username

    def set_profile (self, new_profile):
        """
        Sends a profile string to be saved on the server and associated with
        this USER.
        """
        self.profile = new_profile

    def __unicode__ (self):

        if self.last_name != None and self.last_name != "" and \
           self.first_name != None and self.first_name != "" :
            return "%s, %s" % (self.last_name, self.first_name)

        elif self.last_name != None and self.last_name != "":
            return "%s" % (self.last_name)

        elif self.first_name != None and self.first_name != "":
            return "%s" % (self.first_name)

        else:
            return "%s" % (self.username)

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
