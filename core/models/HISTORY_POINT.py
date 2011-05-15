#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 15, 2011 1:25:13 AM$"

###############################################################################
###############################################################################

from django.db import models

###############################################################################
###############################################################################

## public class HistoryPoint extends Object implements Cloneable
class HISTORY_POINT (models.Model):

    """
    A useful container class that holds TICK objects representing the opening,
    closing, minimum and maximum bid and ask prices.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'history points'

    def __init__ (self, *args, **kwargs):

        super (HISTORY_POINT, self).__init__ (*args, **kwargs)

    ##    java.lang.Object	clone()
    ##
    ##    CandlePoint	getCandlePoint()
    ##    Returns the associated CandlePoint for this FXHistoryPoint.
    ##    FXTick	getClose()
    ##    Returns the FXTick containing the closing bid and ask price for this FXHistoryPoint.
    ##    boolean	getCorrected()
    ##    A flag to indicate whether the FXHistoryPoint has been corrected in the vector context that it is part of.
    ##    FXTick	getMax()
    ##    Returns the FXTick containing the maximum bid and ask price for this FXHistoryPoint.
    ##    FXTick	getMin() 
    ##    Returns the FXTick containing the minimum bid and ask price for this FXHistoryPoint.
    ##    MinMaxPoint	getMinMaxPoint()
    ##    Returns the associated MinMaxPoint for this FXHistoryPoint.
    ##    FXTick	getOpen()
    ##    Returns the FXTick containing the opening bid and ask price for this FXHistoryPoint.
    ##    long	getTimestamp()
    ##    Returns the opening timestamp for this FXHistoryPoint.
    ##    void	setCorrected(boolean aCorrected)
    ##    Set the corrected flag for this FXHistoryPoint
    ##    java.lang.String	toString()
    ##    Returns a String representation of this FXHistoryPoint as follows:
    ##    timestamp max_bid max_ask open_bid open_ask close_bid close_ask min_bid min_ask

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
