#! /usr/bin/python

__author__="hsk81"
__date__ ="$Oct 23, 2011 10:41:51 PM$"

###############################################################################################
###############################################################################################

from django.db.models import *

###############################################################################################
###############################################################################################

class BASE_QUERYSET (query.QuerySet):

    def delete (self, using = settings.DATABASES['default'], *args, **kwargs):

        if not len (self):
            return

        map (lambda obj: obj.delete (using, *args, **kwargs), self)

###############################################################################################
###############################################################################################

class BASE_MANAGER (Manager):

    def get_query_set(self):

        qs = super (BASE_MANAGER,self).get_query_set().filter (delete_date__isnull = True)
        qs.__class__ = BASE_QUERYSET
        return qs

    def all_with_deleted (self):

        qs = super (BASE_MANAGER, self).get_query_set ()
        qs.__class__ = BASE_QUERYSET
        return qs

    def deleted_set (self):

        qs = super (BASE_MANAGER, self).get_query_set ().filter (delete_date__isnull = False)
        qs.__class__ = BASE_QUERYSET
        return qs

    def get (self, *args, **kwargs):

        return self.all_with_deleted ().get (*args, **kwargs)

    def filter (self, *args, **kwargs):
        
        if 'pk' in kwargs:
            qs = self.all_with_deleted ().filter (*args, **kwargs)
        else:
            qs = self.get_query_set ().filter (*args, **kwargs)
            
        qs.__class__ = BASE_QUERYSET
        return qs

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
