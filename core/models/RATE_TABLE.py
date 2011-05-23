#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 11, 2011 9:18:32 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *
from datetime import *

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
        
        self.ip_address = None

    ###########################################################################
    ###########################################################################
    
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

    def get_rate (self, pair):

        return TICK.objects.filter (pair = pair).order_by ('-datetime')[0]

    def logged_in (self):

        sessions = SESSION.objects.filter (
            ip_address = self.ip_address,
            stamp__insert_date__lt = datetime.now (),
            stamp__delete_date__isnull = True
        )

        return bool (sessions)

###############################################################################
###############################################################################

RATE_TABLE.singleton = RATE_TABLE ()

###############################################################################
###############################################################################

class WRAP:

    def invoke (cls, method, args):

        try:
            return getattr (WRAP, method)(cls, method, args)
        
        except Exception, ex:
            return 'EXCEPTION|%s' % ex

    invoke = staticmethod (invoke)

    def get_rate (cls, method, args):

        try:
            q2b = args.split ('/')
            pair = PAIR.objects.get (quote = q2b[0], base = q2b[1])
            tick = RATE_TABLE.singleton.get_rate (pair)

            return '%s|%s|%s|%d|%0.6f|%0.6f' % (cls, method, args,
                tick.unixstamp, tick.bid, tick.ask
            )

        except Exception, ex:
            return 'EXCEPTION|%s' % ex

    get_rate = staticmethod (get_rate)

    def logged_in (cls, method, args):

        RATE_TABLE.singleton.ip_address = args

        try:
            result = '%s|%s|%s|%s' % (cls, method, args,
                RATE_TABLE.singleton.logged_in ()
            )

        except Exception, ex:
            return 'EXCEPTION|%s' % ex

        finally:
            RATE_TABLE.singleton.ip_address = None

        return result

    logged_in = staticmethod (logged_in)

###############################################################################
###############################################################################

RATE_TABLE.invoke = staticmethod (WRAP.invoke)

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
