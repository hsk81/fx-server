#! /usr/bin/python

__author__="hsk81"
__date__ ="$Oct 23, 2011 7:58:06 PM$"

###############################################################################################
###############################################################################################

from managers import *
from time import mktime
from datetime import datetime
from django.db import models
from softdelete.models import *
from softdelete.admin import *

###############################################################################################
###############################################################################################

class BASE_DELETE_RECORD (SoftDeleteRecord):

    class Meta:

        proxy = True
        app_label = 'base'
        verbose_name_plural = 'base delete records'

class BASE_QUERYSET (SoftDeleteQuerySet):

    pass

###############################################################################################
###############################################################################################

class BASE (SoftDeleteObject):

    class Meta:
        
        abstract = True
        app_label = 'base'
        verbose_name_plural = 'bases'

    objects = BASE_MANAGER ()

    ###########################################################################################
    ###########################################################################################

    insert_date = models.DateTimeField (default = datetime.utcnow (), auto_now_add = True)
    update_date = models.DateTimeField (default = datetime.utcnow (), auto_now = True)

    def get_delete_date (self): return self.delete_at
    def set_delete_date (self, value): self.delete_at = value
    delete_date = property (get_delete_date, set_delete_date)

    @property
    def insert_date_unix (self):
        return self.insert_date and int (mktime (self.insert_date.timetuple ()))
    @property
    def update_date_unix (self):
        return self.update_date and int (mktime (self.update_date.timetuple ()))
    @property
    def delete_date_unix (self):
        return self.update_date and int (mktime (self.delete_date.timetuple ()))

    ###########################################################################################
    ###########################################################################################

    def save (self, **kwargs):

        self.update_date = datetime.utcnow ()
        super (BASE, self).save (**kwargs)

    def delete (self, *args, **kwargs):

        self.update_date = datetime.utcnow ()
        super (BASE, self).delete (*args, **kwargs)

    def undelete (self, *args, **kwargs):

        self.update_date = datetime.utcnow ()
        super (BASE, self).undelete (*args, **kwargs)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
