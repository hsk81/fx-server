#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 14, 2011 5:43:02 PM$"

###############################################################################
###############################################################################

from django.db import models
from core.models import *
from datetime import *
from time import *

###############################################################################
###############################################################################

class CLIENT (models.Model):

    """
    A CLIENT object facilitates communication with foreign exchange servers.
    Once connected the CLIENT object provides access to two root objects: USER
    and RATE_TABLE.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'client'

    ###########################################################################
    ###########################################################################

    def __init__ (self, *args, **kwargs):

        super (CLIENT, self).__init__ (*args, **kwargs)

    ###########################################################################
    ###########################################################################

    def get_server_time (self):
        """
        Returns the current time held by the foreign exchange server expressed
        as a unix timestamp.
        """
        return mktime (datetime.now ().timetuple ())

    get_server_time = staticmethod (get_server_time)

    def login (self, username, password, ip_address):
        """
        Attempts to establish a connection to foreign exchange servers.
        """
        users_by_username = USER.objects.filter (username=username)
        users_by_password = USER.objects.filter (password=password)

        if bool (users_by_username):
            if bool (users_by_password):

                user = USER.objects.get (
                    username=username, password=password
                )

                sessions = SESSION.objects.filter (
                    user = user,
                    ip_address__neq = ip_address,
                    stamp__insert_date__lt = datetime.now (),
                    stamp__delete_date__isnull = True
                )

                if not bool (sessions):
                    SESSION.objects.create (
                        user = user,
                        ip_address = ip_address,
                        stamp = STAMP()
                    )

                    return 'CONNECTED'
                else:
                    return 'SESSION_ERROR'
            else:
                return 'INVALID_PASSWORD_ERROR'
        else:
            return 'INVALID_USER_ERROR'

    login = staticmethod (login)

    def logout (self, username, password, ip_address):
        """
        Disconnects from the server.
        """
        users_by_username = USER.objects.filter (username=username)
        users_by_password = USER.objects.filter (password=password)

        if bool (users_by_username):
            if bool (users_by_password):

                user = USER.objects.get (
                    username=username, password=password
                )

                sessions = SESSION.objects.filter (
                    user = user,
                    ip_address = ip_address,
                    stamp__insert_date__lt = datetime.now (),
                    stamp__delete_date__isnull = True
                )

                if bool (sessions):
                    for session in sessions:
                        session.delete_date = datetime.now ()
                        session.save ()

                    return 'DISCONNECTED'
                else:
                    return 'SESSION_ERROR'
            else:
                return 'INVALID_PASSWORD_ERROR'
        else:
            return 'INVALID_USER_ERROR'
    
    logout = staticmethod (logout)

    ###########################################################################
    ###########################################################################

    def __unicode__ (self):

        return "%s" % ((user != None) and user or None)

###############################################################################
###############################################################################

class WRAP:

    def invoke (cls, method, *args):

        return getattr (WRAP, method)(cls, method, *args)

    invoke = staticmethod (invoke)

    def login (cls, method, username, password, ip_address):

        return '%s|%s|%s|%s|%s' % (cls, method, username, password,
            CLIENT.login (username, password, ip_address)
        )

    login = staticmethod (login)

    def logout (cls, method, username, password, ip_address):

        return '%s|%s|%s|%s|%s' % (cls, method, username, password,
            CLIENT.logout (username, password, ip_address)
        )

    logout = staticmethod (logout)

    def get_server_time (cls, method):

        return '%s|%s|%d' % (cls, method,
            CLIENT.get_server_time ()
        )

    get_server_time = staticmethod (get_server_time)

###############################################################################
###############################################################################

CLIENT.invoke = staticmethod (WRAP.invoke)

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
