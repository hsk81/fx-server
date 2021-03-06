__author__ = "hsk81"
__date__ = "$May 23, 2011 11:28:43 PM$"

###############################################################################################
###############################################################################################

from base.models import *
from core.models import *
from django.db import models

###############################################################################################
###############################################################################################

class SESSION (BASE):

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'sessions'

    ###########################################################################################
    ###########################################################################################

    user = models.ForeignKey ('USER', related_name = 'sessions')
    ip_address = models.IPAddressField ()
    token = models.CharField (max_length = 36, unique = True, default = TOKEN.generate)

    ###########################################################################################
    ###########################################################################################

    def __unicode__ (self):

        return "[%s] %s" % (self.update_date, self.ip_address)

###############################################################################################
###############################################################################################
