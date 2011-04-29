#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 22, 2011 2:50:14 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *

###############################################################################
###############################################################################

class STAMP (models.Model):

    """
    TODOC
    """

    class Meta:

        app_label = 'core'

    insert_date = models.DateTimeField (auto_now_add = True)
    update_date = models.DateTimeField (auto_now = True)
    delete_date = models.DateTimeField (null = True)

    def __unicode__ (self):
        """
        Returns string representation for this STAMP.
        """
        return "%s" % self.insert_date

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
