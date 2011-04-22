#! /usr/bin/python

__author__="hsk81"
__date__ ="$Apr 22, 2011 2:50:14 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *

###############################################################################
###############################################################################

class CURRENCY (models.Model):

    """
    TODOC
    """

    class Meta:
    
        app_label = 'core'

    code = models.CharField (max_length = 3)
    name = models.CharField (max_length = 256)

    def __unicode__ (self):
        """
        Returns string representation for this CURRENCY.
        """
        return "%s" % self.code

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
