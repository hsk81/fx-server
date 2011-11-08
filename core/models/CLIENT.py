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
            insert_date__lt = datetime.utcnow (),
            delete_date__isnull = True
        )

        if bool (sessions_with_other_ip_addresses):
            
            return 'SESSION_ERROR'

        sessions_with_same_ip_addresses = SESSION.objects.filter (
            user = user,
            ip_address = ip_address,
            insert_date__lt = datetime.utcnow (),
            delete_date__isnull = True
        )

        if not bool (sessions_with_same_ip_addresses):

            session = SESSION.objects.create (
                user = user,
                ip_address = ip_address
            )

        else:

            for session in sessions_with_same_ip_addresses:

                session.save () ## refresh update_date!

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

            session.delete ()

        return 'DISCONNECTED'
    
###############################################################################################
###############################################################################################

class WRAP:

    def invoke (cls, method, *args):

        return getattr (WRAP, method) (*args)

    invoke = staticmethod (invoke)

    def login (username, password, ip_address):

        return CLIENT ().login (username, password, ip_address)

    login = staticmethod (login)

    def logout (session_token):

        return CLIENT ().logout (session_token)

    logout = staticmethod (logout)

    def refresh (session_token):

        return CLIENT ().refresh (session_token)

    refresh = staticmethod (refresh)

    def get_server_time ():

        return CLIENT ().server_time

    get_server_time = staticmethod (get_server_time)

###############################################################################################
###############################################################################################

CLIENT.invoke = staticmethod (WRAP.invoke)

###############################################################################################
###############################################################################################
