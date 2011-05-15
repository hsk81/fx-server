#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 14, 2011 5:43:02 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *
from datetime import *
from time import *

###############################################################################
###############################################################################

## public abstract class FXClient extends java.util.Observable
class CLIENT (models.Model):

    """
    A CLIENT object facilitates communication with foreign exchange servers.
    Once connected the CLIENT object provides access to two root objects: USER
    and RATE_TABLE.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'client'

    ###########################################################################
    ###########################################################################

    def __init__ (self, *args, **kwargs):

        super (CLIENT, self).__init__ (*args, **kwargs)

        self.user = None
        self.rate_table = None
        self.state = None
        self.timeout = None

        self.observers = []

    ###########################################################################
    ###########################################################################

    ## User getUser()
    def get_user (self):
        """
        Returns the USER object currently connected to the foreign exchange
        server.
        """
        return self.user

    ## RateTable getRateTable()
    def get_rate_table (self):
        """
        Returns the RATE_TALBE object.
        """
        return self.rate_table

    ## long getServerTime()
    def get_server_time (self):
        """
        Returns the current time held by the foreign exchange server expressed
        as a unix timestamp.
        """
        return mktime (datetime.now ().timetuple ())

    ## boolean isLoggedIn()
    def is_logged_in (self):
        """
        Returns true if a connection exists with the server, false otherwise.
        """
        return self.user != None and self.rate_table != None
    
    ## void login(java.lang.String username, java.lang.String password)
    def login (self, username, password):
        """
        Attempts to establish a connection to foreign exchange servers.
        """
        self.user = USER.objects.get (username=username, password=password)
        self.rate_table = RATE_TABLE ()

    ## void logout()
    def logout (self):
        """
        Disconnects from the server.
        """
        self.user = None
        self.rate_table = None
    
    ## void setProxy(boolean state)
    def set_proxy (self, state):
        """
        Sets the proxy status for future connections to the server.
        """
        self.state = state

    ## void setTimeout(int timeout)
    def set_timeout (self, timeout):
        """
        Sets the timeout for server response in seconds.
        """
        self.timeout = timeout
    
    ###########################################################################
    ###########################################################################

    ##
    ## TODO: Check implementation with pythonic approaches!
    ##

    def add_observer (self, observer):

        self.observers.add (observer)

    def count_observers (self):

        return self.observer.count ()

    def delete_observer (self, observer):

        self.observers.remove (observer)

    def delete_observers (self):

        self.observers = []

    def has_changed (self):

        raise NotImplementedError

    def notify_observers (self):

        ##
        ## TODO: Check parallel approaches!
        ##

        for observer in self.observers:

            observer.update ()

    ###########################################################################
    ###########################################################################

    ## java.lang.String toString()
    def __unicode__ (self):

        return "%s" % ((self.user != None) and self.user or None)

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
