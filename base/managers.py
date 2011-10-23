#! /usr/bin/python

__author__="hsk81"
__date__ ="$Oct 23, 2011 10:41:51 PM$"

###############################################################################################
###############################################################################################

from django.db import models

###############################################################################################
###############################################################################################

class BASE_MANAGER (models.Manager):

    def get_query_set (self, with_deleted = True):

        if self.model:
            if with_deleted:
                return super (BASE_MANAGER, self).get_query_set ()
            else:
                return super (BASE_MANAGER, self).get_query_set () \
                    .filter (delete_date__isnull = True)

    def aggregate (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).aggregate (*args, **kwargs)
    def all (self, with_deleted = False):
        return self.get_query_set (with_deleted = with_deleted).all ()
    def annotate (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).annotate (*args, **kwargs)
    def complex_filter (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).complex_filter (*args, **kwargs)
    def contribute_to_class (self, model, name):
        return super (BASE_MANAGER, self).contribute_to_class (model, name)
    def count (self, with_deleted = False):
        return self.get_query_set (with_deleted = with_deleted).count (*args, **kwargs)
    def create (self, **kwargs):
        return super (BASE_MANAGER, self).create (**kwargs)
    def dates (self, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).dates (*args, **kwargs)
    def db_manager (self, using):
        return super (BASE_MANAGER, self).db_manager (using)
    def defer (self, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).defer (*args, **kwargs)
    def distinct (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).distinct (*args, **kwargs)
    def exclude (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).exclude (*args, **kwargs)
    def exists (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).exists (*args, **kwargs)
    def extra (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).extra (*args, **kwargs)
    def filter (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).filter (*args, **kwargs)
    def get (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).get (*args, **kwargs)
    def get_empty_query_set (self):
        return super (BASE_MANAGER, self).get_empty_query_set ()
    def get_or_create (self, with_deleted = False, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).get_or_create (**kwargs)
    def in_bulk (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).in_bulk (*args, **kwargs)
    def iterator (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).iterator (*args, **kwargs)
    def latest (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).latest (*args, **kwargs)
    def none (self, with_deleted = False):
        return self.get_query_set (with_deleted = with_deleted).none (*args, **kwargs)
    def only (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).only (*args, **kwargs)
    def order_by (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).order_by (*args, **kwargs)
    def raw (self, raw_query, params=None, *args, **kwargs):
        return super (BASE_MANAGER, self).raw (raw_query, params, *args, **kwargs)
    def reverse (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).reverse (*args, **kwargs)
    def select_related (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).select_related (*args, **kwargs)
    def update (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).update (*args, **kwargs)
    def using (self, *args, **kwargs):
        return super (BASE_MANAGER, self).using (*args, **kwargs)
    def values (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).values (*args, **kwargs)
    def values_list (self, with_deleted = False, *args, **kwargs):
        return self.get_query_set (with_deleted = with_deleted).values_list (*args, **kwargs)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass