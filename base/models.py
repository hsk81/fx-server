#! /usr/bin/python

__author__="hsk81"
__date__ ="$Oct 23, 2011 7:58:06 PM$"

###############################################################################################
###############################################################################################

from managers import *
from time import mktime
from django.db import models
from datetime import datetime
from softdelete.models import *

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

    insert_at = models.DateTimeField (default = datetime.utcnow (), auto_now_add = True)
    update_at = models.DateTimeField (default = datetime.utcnow (), auto_now = True)

    def get_insert_date (self): return self.insert_at
    def set_insert_date (self, value): self.insert_at = value
    insert_date = property (get_insert_date, set_insert_date)

    def get_update_date (self): return self.update_at
    def set_update_date (self, value): self.update_at = value
    update_date = property (get_update_date, set_update_date)

    def get_delete_date (self): return self.deleted_at
    def set_delete_date (self, value): self.deleted_at = value
    delete_date = property (get_delete_date, set_delete_date)

    ###########################################################################################
    ###########################################################################################

    @property
    def insert_date_unix (self):
        return self.insert_at and int (mktime (self.insert_at.timetuple ()))
    @property
    def update_date_unix (self):
        return self.update_at and int (mktime (self.update_at.timetuple ()))
    @property
    def delete_date_unix (self):
        return self.update_at and int (mktime (self.delete_at.timetuple ()))

    ###########################################################################################
    ###########################################################################################

    def save (self, **kwargs):

        self.update_at = datetime.utcnow ()
        super (BASE, self).save (**kwargs)

    def delete (self, *args, **kwargs):

        self.update_at = datetime.utcnow ()
        super (BASE, self).delete (*args, **kwargs)

    def undelete (self, *args, **kwargs):

        self.update_at = datetime.utcnow ()
        super (BASE, self).undelete (*args, **kwargs)

###############################################################################################
###############################################################################################

class BASE_DELETE_RECORD (SoftDeleteRecord):

    class Meta:

        proxy = True
        app_label = 'base'
        verbose_name_plural = 'base delete records'

###############################################################################################
###############################################################################################

class BASE_QUERYSET (SoftDeleteQuerySet):

    pass

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
