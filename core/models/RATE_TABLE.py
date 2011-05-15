#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 11, 2011 9:18:32 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *

###############################################################################
###############################################################################

class RATE_TABLE (models.Model):

    """
    The RATE_TABLE object holds all incoming rate information. A rate table is
    used to obtain rate info (quotes for currency pairs) and history data for
    these as well.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'rate tables'

    ###########################################################################
    ###########################################################################

    def __init__ (self, *args, **kwargs):

        super (RATE_TABLE, self).__init__ (*args, **kwargs)
        self.event_manager = EVENT_MANAGER ()

    ## java.util.Vector getCandles(FXPair pair, long interval, int numTicks)
    def get_candles (self, pair, interval, num_ticks):
        """
        Obtain the current history (in terms of CANDLE_POINTs) of a given
        currency pair at a given millisecond interval of a particular length
        (num_ticks).
        """
        raise NotImplementedError

    ## FXEventManager getEventManager()
    def get_event_manager (self):
        """
        Get the event manager for this RATE_TABLE.
        """
        return self.event_manager

    ## java.util.Vector getHistory(FXPair pair, long interval, int numTicks)
    def get_history (self, pair, interval, num_ticks):
        """
        Obtain the current history (in terms of HISTORY_POINTs) of a given
        currency pair at a given millisecond interval of a particular length
        (num_ticks).
        """
        raise NotImplementedError

    ## java.util.Vector getMinMaxs(FXPair pair, long interval, int numTicks)
    def get_min_maxs (self, pair, interval, num_ticks):
        """
        Obtain the current history (in terms of MIN_MAX_POINTs) of a given
        currency pair at a given millisecond interval of a particular length
        (num_ticks).
        """
        raise NotImplementedError

    ## FXTick getRate(FXPair pair)
    def get_rate (pair):
        """
        Returns the most recent TICK for the given PAIR.
        """
        return TICK.objects.filter (pair=pair).order_by ('-datetime')[0]

    ## boolean loggedIn()
    def logged_in (self):
        """
        Check whether the session is active.
        """
        return True

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
