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

        map (lambda obj: obj.delete (using, *args, **kwargs), self)

###############################################################################################
###############################################################################################

class BASE_MANAGER (Manager):

    def get_query_set (self):

        return self.with_deleted ().filter (delete_date__isnull = 1)

    def only_deleted (self):

        return self.with_deleted ().filter (delete_date__isnull = 0)

    def with_deleted (self):

        qs = super (BASE_MANAGER, self).get_query_set ()
        qs.__class__ = BASE_QUERYSET
        return qs

    def get (self, *args, **kwargs):

        return self.with_deleted ().get (*args, **kwargs)

    def filter (self, *args, **kwargs):
        
        if 'pk' in kwargs:
            qs = self.with_deleted ().filter (*args, **kwargs)
        else:
            qs = self.get_query_set ().filter (*args, **kwargs)
            
        return qs

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
