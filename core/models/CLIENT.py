#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$May 14, 2011 5:43:02 PM$"

###############################################################################################
###############################################################################################

from time import *
from datetime import *
from base.models import *
from core.models import *

###############################################################################################
###############################################################################################

class CLIENT (BASE):

    ###########################################################################################
    ###########################################################################################

    server_time = property (lambda self: mktime (datetime.now ().timetuple ()))

    ###########################################################################################
    ###########################################################################################

    def login (self, username, password, ip_address): ##TODO: DB transactions?

        users_by_username = USER.objects.filter (username = username)
        if not bool (users_by_username): return 'INVALID_USER_ERROR'

        users_by_password = USER.objects.filter (username = username, password = password)
        if not bool (users_by_password): return 'INVALID_PASSWORD_ERROR'

        user = USER.objects.get (
            username = username, password = password
        )

        sessions_with_other_ip_addresses = SESSION.objects.filter (
            user = user,
            ip_address__lt = ip_address,
            ip_address__gt = ip_address,
            stamp__insert_date__lt = datetime.now (),
            stamp__delete_date__isnull = True
        )

        if bool (sessions_with_other_ip_addresses):
            return 'SESSION_ERROR'

        sessions_with_same_ip_addresses = SESSION.objects.filter (
            user = user,
            ip_address = ip_address,
            stamp__insert_date__lt = datetime.now (),
            stamp__delete_date__isnull = True
        )

        if not bool (sessions_with_same_ip_addresses):

            session = SESSION.objects.create (
                user = user,
                ip_address = ip_address,
                stamp = STAMP.objects.create ()
            )

        else:

            for session in sessions_with_same_ip_addresses:

                old_stamp = session.stamp
                new_stamp = STAMP.objects.create ()
                session.stamp = new_stamp
                session.save ()
                old_stamp.delete ()

        return 'CONNECTED|%s' % session.token

    def refresh (self, session_token):

        sessions = SESSION.objects.filter (token = session_token)
        if not bool (sessions): return 'SESSION_ERROR'

        for session in sessions:

            result = self.login (
                session.user.username,
                session.user.password,
                session.ip_address
            )

        return result

    def logout (self, session_token):

        for session in SESSION.objects.filter (token = session_token):

            session.stamp.delete_date = datetime.now ()
            session.save ()

        return 'DISCONNECTED'
    
###############################################################################################
###############################################################################################

class WRAP:

    def invoke (cls, method, *args):

        return getattr (WRAP, method)(cls, method, *args)

    invoke = staticmethod (invoke)

    def login (cls, method, username, password, ip_address):

        return '%s|%s|%s|%s|%s|%s' % (cls, method, username, password, ip_address,
            CLIENT ().login (username, password, ip_address)
        )

    login = staticmethod (login)

    def logout (cls, method, session_token):

        return '%s|%s|%s|%s' % (cls, method, session_token,
            CLIENT ().logout (session_token)
        )

    logout = staticmethod (logout)

    def refresh (cls, method, session_token):

        return '%s|%s|%s|%s' % (cls, method, session_token,
            CLIENT ().refresh (session_token)
        )

    refresh = staticmethod (refresh)

    def get_server_time (cls, method):

        return '%s|%s|%d' % (cls, method, CLIENT ().server_time)

    get_server_time = staticmethod (get_server_time)

###############################################################################################
###############################################################################################

CLIENT.invoke = staticmethod (WRAP.invoke)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
