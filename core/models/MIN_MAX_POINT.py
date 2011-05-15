#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 15, 2011 1:32:17 AM$"

###############################################################################
###############################################################################

from django.db import models

###############################################################################
###############################################################################

## public class MinMaxPoint extends Object implements Cloneable
class MIN_MAX_POINT (models.Model):

    """
    MIN_MAX_POINT class is a container for min/max graph information. A
    MIN_MAX_POINT is calculated from a HISTORTY_POINT directly.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'min max points'

    def __init__ (self, *args, **kwargs):

        super (MIN_MAX_POINT, self).__init__ (*args, **kwargs)

    ##    java.lang.Object	clone()
    ##
    ##    double	getMax() 
    ##    Return the maximum ask price for the interval
    ##    double	getMin() 
    ##    Return the minimum bid price for the interval
    ##    long	getTimestamp() 
    ##    Return the server timestamp for this MinMaxPoint (time in seconds after the beginning of the epoch).
    ##    java.lang.String	toString() 
    ##    Convert MinMaxPoint to a string
    ##
    
###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
