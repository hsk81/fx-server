#! /usr/bin/python

__author__="hsk81"
__date__ ="$Oct 23, 2011 7:58:06 PM$"

###############################################################################################
###############################################################################################

from managers import *
from time import mktime
from datetime import datetime
from django.db import models

###############################################################################################
###############################################################################################

class BASE (models.Model):

    class Meta:

        abstract = True
        app_label = 'base'
        verbose_name_plural = 'bases'

    objects = BASE_MANAGER ()

    ###########################################################################################
    ###########################################################################################

    insert_date = models.DateTimeField (default = datetime.now (), auto_now_add = True)
    update_date = models.DateTimeField (default = datetime.now (), auto_now = True)
    delete_date = models.DateTimeField (null = True, blank = True)

    @property
    def insert_date_unix (self):
        return self.insert_date and '%d' % mktime (self.insert_date)
    @property
    def update_date_unix (self):
        return self.update_date and '%d' % mktime (self.update_date)
    @property
    def delete_date_unix (self):
        return self.delete_date and '%d' % mktime (self.delete_date)

    ###########################################################################################
    ###########################################################################################

    def save (self):

        super (BASE, self).save ()

    def delete (self):
        
        if not self.delete_date:
            self.update_date = datetime.now ()
            self.delete_date = datetime.now ()
            self.save ()
        else:
            pass ## no delete!

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
