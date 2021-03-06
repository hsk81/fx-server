__author__ = "hsk81"
__date__ = "$May 11, 2011 9:18:32 PM$"

###############################################################################################
###############################################################################################

from datetime import *
from core.models import *

###############################################################################################
###############################################################################################

class RATE_TABLE:

    def get_history (pair, interval, num_ticks):

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

        return TICK.objects.filter (pair = pair).order_by ('-datetime')[0]

    get_rate = staticmethod (get_rate)

    def logged_in (ip_address):

        sessions = SESSION.objects.filter (
            ip_address = ip_address,
            stamp__insert_date__lt = datetime.now (),
            stamp__delete_date__isnull = True
        )

        return bool (sessions)

    logged_in = staticmethod (logged_in)

###############################################################################################
###############################################################################################

class WRAP:

    def invoke (cls, method, *args):

        return getattr (WRAP, method) (*args)

    invoke = staticmethod (invoke)

    def get_rate (quote, base):

        pair = PAIR.objects.get (quote = quote, base = base)
        tick = RATE_TABLE.get_rate (pair)

        return '%d|%0.6f|%0.6f' % (tick.unixstamp, tick.bid, tick.ask)

    get_rate = staticmethod (get_rate)

    def logged_in (ip_address):

        return RATE_TABLE.logged_in (ip_address)

    logged_in = staticmethod (logged_in)

    def get_history (quote, base, interval, num_ticks):

        pair = PAIR.objects.get (quote = quote, base = base)
        history = RATE_TABLE.get_history (pair, int (interval), int (num_ticks))

        ts = ['%d|%0.6f|%0.6f|%0.6f|%0.6f|%0.6f|%0.6f|%0.6f|%0.6f' % (
            opn.unixstamp,
            opn.bid, opn.ask,
            clo.bid, clo.ask,
            min.bid, min.ask,
            max.bid, max.ask
        ) for opn, clo, min, max in history]

        return '|'.join (ts)

    get_history = staticmethod (get_history)

###############################################################################################
###############################################################################################

RATE_TABLE.invoke = staticmethod (WRAP.invoke)

###############################################################################################
###############################################################################################
