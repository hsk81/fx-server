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

    ###########################################################################
    ###########################################################################
    
    def get_history (pair, interval, num_ticks):
        """
        Obtain the current history (in terms of HISTORY_POINTs) of a given
        currency pair at a given millisecond interval of a particular length
        (num_ticks).
        """
        result = []
        
        td = timedelta (0,0,1000 * interval)
        t0 = TICK.objects.filter (pair = pair).latest ('datetime').datetime
        t1 = t0 - td

        for _ in range (num_ticks):

            ticks = TICK.objects \
                .filter (pair = pair, datetime__lte = t0, datetime__gt = t1) \
                .order_by ('-datetime')

            if ticks.count () > 0:

                opn = ticks[0]
                min = opn
                max = opn

                for tick in ticks:

                    min = (min.mean < tick.mean) and min or tick
                    max = (max.mean > tick.mean) and max or tick

                result.append ((opn, tick, min, max))
                t0 = t1; t1 = t0 - td

            else: break

        return result

    get_history = staticmethod (get_history)
    
    def get_rate (pair):
        """
        Returns the most recent TICK for the given PAIR.
        """
        return TICK.objects.filter (pair = pair).order_by ('-datetime')[0]

    get_rate = staticmethod (get_rate)

    def logged_in (ip_address):
        """
        Check whether the session is active.
        """
        sessions = SESSION.objects.filter (
            ip_address = ip_address,
            stamp__insert_date__lt = datetime.now (),
            stamp__delete_date__isnull = True
        )

        return bool (sessions)

    logged_in = staticmethod (logged_in)

###############################################################################
###############################################################################

class WRAP:

    def invoke (cls, method, *args):

        try:
            return getattr (WRAP, method)(cls, method, *args)
        
        except Exception, ex:
            return 'EXCEPTION|%s' % ex

    invoke = staticmethod (invoke)

    def get_rate (cls, method, quote, base):

        try:
            pair = PAIR.objects.get (quote = quote, base = base)
            tick = RATE_TABLE.get_rate (pair)

            return '%s|%s|%s|%s|%d|%0.6f|%0.6f' % (cls, method, quote, base,
                tick.unixstamp, tick.bid, tick.ask
            )
                
        except Exception, ex:
            return 'EXCEPTION|%s' % ex

    get_rate = staticmethod (get_rate)

    def logged_in (cls, method, ip_address):

        try:
            result = '%s|%s|%s|%s' % (cls, method, ip_address,
                RATE_TABLE.logged_in (ip_address)
            )

        except Exception, ex:
            return 'EXCEPTION|%s' % ex

        return result

    logged_in = staticmethod (logged_in)

    def get_history (cls, method, quote, base, interval, num_ticks):

        try:
            pair = PAIR.objects.get (quote = quote, base = base)
            
            history = RATE_TABLE.get_history (
                 pair, int (interval), int (num_ticks)
            )

            ts = ['%d|%0.6f|%0.6f|%0.6f|%0.6f|%0.6f|%0.6f|%0.6f|%0.6f' % (
                opn.unixstamp,
                opn.bid, opn.ask,
                clo.bid, clo.ask,
                min.bid, min.ask,
                max.bid, max.ask
            ) for opn, clo, min, max in history]

            return '%s|%s|%s|%s|%s|%s|%s' % (cls, method,
                quote, base, interval, num_ticks, '|'.join (ts)
            )

        except Exception, ex:
            return 'EXCEPTION|%s' % ex

    get_history = staticmethod (get_history)

###############################################################################
###############################################################################

RATE_TABLE.invoke = staticmethod (WRAP.invoke)

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
