#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 8, 2011 11:36:39 AM$"

###############################################################################
###############################################################################

from django.db import models

###############################################################################
###############################################################################

## public class CandlePoint extends Object implements Cloneable
class CANDLE_POINT (models.Model):

    """
    A CANDLE_POINT is a container for candle information. It is calculated from
    a HISTORY_POINT directly.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'candle points'

    ## CandlePoint(long timestamp,
    ##     double open, double close, double min, double max
    ## )
    def __init__ (self, *args, **kwargs):
        """
        ???
        """
        super (CANDLE_POINT, self).__init__ (*args, **kwargs)

    ## java.lang.Object clone()
    def clone (self):
        """
        ???
        """
        raise NotImplementedError

    ## double getClose()
    def get_close (self):
        """
        ???
        """
        raise NotImplementedError

    ## double getMax()
    def get_max (self):
        """
        ???
        """
        raise NotImplementedError
    
    ## double getMin()
    def get_min (self):
        """
        ???
        """
        raise NotImplementedError

    ## double getOpen()
    def get_open (self):
        """
        ???
        """
        raise NotImplementedError

    ## long getTimestamp()
    def get_timestamp (self):
        """
        ???
        """
        raise NotImplementedError

    ## java.lang.String toString()
    def __unicode__ (self):
        """
        ???
        """
        raise NotImplementedError

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
