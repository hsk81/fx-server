#! /usr/bin/python

__author__="hsk81"
__date__ ="$Oct 23, 2011 7:58:06 PM$"

###############################################################################################
###############################################################################################

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

    insert_date = models.DateTimeField (default = datetime.utcnow (), auto_now_add = True)
    update_date = models.DateTimeField (default = datetime.utcnow (), auto_now = True)
    delete_date = models.DateTimeField (blank = True, null = True, default = None)

    ###########################################################################################
    ###########################################################################################

    @property
    def insert_date_unix (self):
        return self.insert_date and int (mktime (self.insert_date.timetuple ()))
    @property
    def update_date_unix (self):
        return self.update_date and int (mktime (self.update_date.timetuple ()))
    @property
    def delete_date_unix (self):
        return self.delete_date and int (mktime (self.delete_date.timetuple ()))
    
    ###########################################################################################
    ###########################################################################################
    
    def get_deleted (self):
        
        return self.delete_date != None

    def set_deleted (self, value):

        if not self.delete_date:
            if value: self.delete_date = datetime.utcnow ()
            else: pass
            
        else:
            if not value: self.delete_date = None
            else: pass

    deleted = property (get_deleted, set_deleted)

    ###########################################################################################
    ###########################################################################################

    def delete(self, *args, **kwargs):
        
        if self.delete_date:
            super (BASE, self).delete (*args, **kwargs)

        else:
            using = kwargs.get ('using', settings.DATABASES['default'])
            
            models.signals.pre_delete.send (
                sender =self.__class__, instance = self, using = using)

            self.update_date = datetime.utcnow ()
            self.delete_date = self.update_date
            self.save ()

            for related in self._meta.get_all_related_objects ():                
                self._do_delete (related)

            models.signals.post_delete.send (
                sender = self.__class__, instance = self, using = using)

    def _do_delete (self, related):

        try:
            getattr (self, related.get_accessor_name ()).all ().delete ()
        except:
            getattr (self, related.get_accessor_name ()).__class__.objects.all ().delete ()

    ###########################################################################################
    ###########################################################################################

    def save (self, **kwargs):

        self.update_date = datetime.utcnow ()
        super (BASE, self).save (**kwargs)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
