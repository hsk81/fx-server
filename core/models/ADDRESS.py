#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 22, 2011 2:50:14 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *

###############################################################################
###############################################################################

class ADDRESS (models.Model):

    """
    ...
    """
    
    class Meta:

        app_label = 'core'
        verbose_name_plural = 'addresses'

    line1 = models.CharField (max_length = 256)
    line2 = models.CharField (max_length = 256, blank = True, default = '')
    zip = models.CharField (max_length = 256)
    city = models.CharField (max_length = 256)
    country = models.CharField (max_length = 256)

    def full_address (self, show_blank_line2 = False):
        """
        Returns string representation for this ADDRESS.
        """
        if show_blank_line2:
            return "%s\n%s\n%s %s\n%s" % (
                self.line1, self.line2, self.zip, self.city, self.country
            )
        else:
            return (self.line2 != "") and (
                "%s\n%s\n%s %s\n%s" % (
                    self.line1, self.line2, self.zip, self.city, self.country
                )
            ) or (
                "%s\n%s %s\n%s" % (
                    self.line1, self.zip, self.city, self.country
                )
            )

    def short_address (self, show_blank_line2 = False):
        """
        Returns string representation for this ADDRESS.
        """
        if show_blank_line2:
            return "%s\n%s\n%s %s" % (
                self.line1, self.line2, self.zip, self.city
            )
        else:
            return (self.line2 != "") and (
                "%s\n%s\n%s %s" % (self.line1, self.line2, self.zip, self.city)
            ) or (
                "%s\n%s %s" % (self.line1, self.zip, self.city)
            )


    def __unicode__ (self):
        """
        Returns string representation for this ADDRESS.
        """
        return self.short_address ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
