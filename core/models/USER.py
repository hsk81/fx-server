__author__ = "hsk81"
__date__ = "$Apr 22, 2011 2:50:14 PM$"

###############################################################################################
###############################################################################################

from time import mktime
from base.models import *
from core.models import *
from django.db import models
from django.contrib import auth

###############################################################################################
###############################################################################################

class USER (BASE, auth.models.User):

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'users'

    ###########################################################################################
    ###########################################################################################

    address = models.ForeignKey (ADDRESS, related_name = 'users')
    phone = models.CharField (max_length = 256)
    profile = models.CharField (max_length = 256, blank = True, default = '')

    ###########################################################################################
    ###########################################################################################

    @property
    def info (self):

        return [
            self.id,
            self.username,
            self.address.short_address (delimiter = ', '),
            int (mktime (self.date_joined.timetuple ())),
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
        
    ###########################################################################################
    ###########################################################################################

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

        return getattr (WRAP, method) (*args)

    invoke = staticmethod (invoke)

    def get_info (session_token):

        session = SESSION.objects.get (token = session_token, delete_date__isnull = True)

        return '|'.join (map (
            lambda value: value and str (value) or str (None), session.user.info
        ))

    get_info = staticmethod (get_info)

    def get_accounts (session_token):

        session = SESSION.objects.get (token = session_token, delete_date__isnull = True)
        return '|'.join (map (lambda account: str (account.id), session.user.accounts.all ()))

    get_accounts = staticmethod (get_accounts)

###############################################################################################
###############################################################################################

USER.invoke = staticmethod (WRAP.invoke)

###############################################################################################
###############################################################################################
