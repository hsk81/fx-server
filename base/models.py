#! /usr/bin/python

__author__="hsk81"
__date__ ="$Oct 23, 2011 7:58:06 PM$"

###############################################################################################
###############################################################################################

import signals
import managers

from time import mktime
from datetime import datetime
from django.db import models
from django.conf import settings

###############################################################################################
###############################################################################################

class BASE (models.Model):

    class Meta:
        
        abstract = True
        app_label = 'base'
        verbose_name_plural = 'bases'
        
    objects = managers.BASE_MANAGER ()

    ###########################################################################################
    ###########################################################################################

    deleted_at = models.DateTimeField (blank=True, null=True, default=None)
    insert_at = models.DateTimeField (default = datetime.utcnow (), auto_now_add = True)
    update_at = models.DateTimeField (default = datetime.utcnow (), auto_now = True)

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
    
    def get_deleted(self):
        
        return self.deleted_at != None

    def set_deleted(self, value):

        if value and not self.deleted_at:
            self.deleted_at = datetime.utcnow ()
        elif not value and self.deleted_at:
            self.deleted_at = None

    deleted = property (get_deleted, set_deleted)

    ###########################################################################################
    ###########################################################################################

    def _do_delete (self, related):

        try:
            getattr (self, related.get_accessor_name ()).all ().delete ()
        except:
            getattr (self, related.get_accessor_name ()).__class__.objects.all ().delete ()

    def delete(self, *args, **kwargs):
        
        if self.deleted_at:
            super (BASE, self).delete (*args, **kwargs)

        else:
            using = kwargs.get ('using', settings.DATABASES['default'])
            
            models.signals.pre_delete.send (
                sender =self.__class__, instance = self, using = using)
            signals.pre_base_delete.send (
                sender = self.__class__, instance = self, using = using)

            self.update_at = datetime.utcnow ()
            self.deleted_at = datetime.utcnow ()
            self.save ()

            for related in self._meta.get_all_related_objects ():                
                self._do_delete (related)

            models.signals.post_delete.send (
                sender = self.__class__, instance = self, using = using)
            signals.post_base_delete.send (
                sender = self.__class__, instance = self, using = using)

    ###########################################################################################
    ###########################################################################################

    def save (self, **kwargs):

        self.update_at = datetime.utcnow ()
        super (BASE, self).save (**kwargs)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
