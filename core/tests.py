__author__ = "hsk81"
__date__ ="$Oct 29, 2011 3:01:55 PM$"

###############################################################################################
###############################################################################################

from core.models import *
from django.test import TestCase

###############################################################################################
###############################################################################################

class CORE_TEST (TestCase):

    def assertDeleted (self, base, objects, with_reload = True):

        if with_reload:
            base = base.reload (objects)
            
        self.assertTrue (base.deleted)

    def test_soft_delete (self):

        users = USER.objects.all ()
        user = users[0]
        self.assertFalse (user.deleted)

        accounts = ACCOUNT.objects.all ()
        account0 = accounts[0]
        self.assertFalse (account0.deleted)
        account1 = accounts[1]
        self.assertFalse (account1.deleted)

        user.delete () ## soft delete
        self.assertDeleted (user, USER.objects)
        self.assertDeleted (account0, ACCOUNT.objects)
        self.assertDeleted (account1, ACCOUNT.objects)

    def test_soft_delete_twice (self):

        users = USER.objects.all ()
        user = users[0]
        self.assertFalse (user.deleted)

        accounts = ACCOUNT.objects.all ()
        account0 = accounts[0]
        self.assertFalse (account0.deleted)
        account1 = accounts[1]
        self.assertFalse (account1.deleted)

        user.delete () ## soft delete
        user.delete () ## soft delete
        self.assertDeleted (user, USER.objects)
        self.assertDeleted (account0, ACCOUNT.objects)
        self.assertDeleted (account1, ACCOUNT.objects)

    def test_hard_delete (self):

        users = USER.objects.all ()
        user = users[0]
        self.assertFalse (user.deleted)

        accounts = ACCOUNT.objects.all ()
        account0 = accounts[0]
        self.assertFalse (account0.deleted)
        account1 = accounts[1]
        self.assertFalse (account1.deleted)

        user.delete (hard = True) ## hard delete
        users = USER.objects.all ()
        self.assertTrue (len (users) == 0)
        accounts = ACCOUNT.objects.all ()
        self.assertTrue (len (accounts) == 0)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
