#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 23, 2011 11:28:43 PM$"

###############################################################################################
###############################################################################################

from django.db import models
from core.models import *

###############################################################################################
###############################################################################################

class SESSION (models.Model):

    """
    An SESSION object represents a session.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'sessions'

    ###########################################################################################
    ###########################################################################################

    def __init__ (self, *args, **kwargs):

        super (SESSION, self).__init__ (*args, **kwargs)

    ###########################################################################################
    ###########################################################################################

    stamp = models.ForeignKey ('STAMP')
    user = models.ForeignKey ('USER')
    ip_address = models.IPAddressField ()
    token = models.CharField (max_length = 36, unique = True, default = TOKEN.generate)

    ###########################################################################################
    ###########################################################################################

    def __unicode__ (self):

        return "[%s] %s" % (self.stamp, self.ip_address)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
