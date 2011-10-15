#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 22, 2011 2:50:14 PM$"

###############################################################################################
###############################################################################################

from core.models import *
from django.db import models
from datetime import datetime
from django.contrib import auth

###############################################################################################
###############################################################################################

class USER (auth.models.User):

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'users'

    stamp = models.ForeignKey (STAMP, editable = False)
    address = models.ForeignKey (ADDRESS)
    phone = models.CharField (max_length = 256)
    profile = models.CharField (max_length = 256, blank = True, default = '')

    ###########################################################################################
    ###########################################################################################

    def save (self):

        if not self.id:
            self.stamp = STAMP.objects.create ()
        else:
            self.stamp.update_date = datetime.now ()
            self.stamp.save ()

        super (ACCOUNT, self).save ()

    def delete (self):

        if not self.stamp.delete_date:
            self.stamp.update_date = datetime.now ()
            self.stamp.delete_date = datetime.now ()
            self.stamp.save ()
        else:
            pass ## no delete

    ###########################################################################################
    ###########################################################################################

    @property
    def insert_date (self): return self.stamp.insert_date
    @property
    def update_date (self): return self.stamp.update_date
    @property
    def delete_date (self): return self.stamp.delete_date

    @property
    def unix_insert_date (self): return self.stamp.unix_insert_date
    @property
    def unix_update_date (self): return self.stamp.unix_update_date
    @property
    def unix_delete_date (self): return self.stamp.unix_delete_date

    ###########################################################################################
    ###########################################################################################
    
    @property
    def info (self):

        return [
            self.id,
            self.username,
            self.address.short_address (delimiter = ', '),
            self.unix_insert_date,
            self.email,
            self.fullname,
            self.password,
            self.phone,
            self.profile
        ]

    @property
    def fullname (self):

        if self.last_name != None and self.last_name != "" and \
           self.first_name != None and self.first_name != "":
            return "%s, %s" % (self.last_name, self.first_name)

        elif self.last_name != None and self.last_name != "":
            return "%s" % (self.last_name)

        elif self.first_name != None and self.first_name != "":
            return "%s" % (self.first_name)

        else:
            return None
        
    def __unicode__ (self):

        if self.last_name != None and self.last_name != "" and \
           self.first_name != None and self.first_name != "":
            return "%s, %s" % (self.last_name, self.first_name)

        elif self.last_name != None and self.last_name != "":
            return "%s" % (self.last_name)

        elif self.first_name != None and self.first_name != "":
            return "%s" % (self.first_name)

        else:
            return "%s" % (self.username)

###############################################################################################
###############################################################################################

class WRAP:

    def invoke (cls, method, *args):

        return getattr (WRAP, method)(cls, method, *args)

    invoke = staticmethod (invoke)

    def get_info (cls, method, session_token):

        session = SESSION.objects.get (
            token = session_token, stamp__delete_date__isnull = True
        )

        return '%s|%s|%s|%s' % (cls, method, session_token, '|'.join (
            map (lambda value: value and str (value) or str (None), session.user.info)
        ))

    get_info = staticmethod (get_info)

    def get_accounts (cls, method, session_token):

        session = SESSION.objects.get (
            token = session_token, stamp__delete_date__isnull = True
        )

        return '%s|%s|%s|%s' % (cls, method, session_token,
            '|'.join (map (lambda account: str (account.id), session.user.accounts.all ()))
        )

    get_accounts = staticmethod (get_accounts)

###############################################################################################
###############################################################################################

USER.invoke = staticmethod (WRAP.invoke)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
