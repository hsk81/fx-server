__author__ = "hsk81"
__date__ ="$Oct 29, 2011 3:01:55 PM$"

###############################################################################################
###############################################################################################

from core.models import *
from django.test import TestCase

###############################################################################################
###############################################################################################

class CORE_TEST (TestCase):

    ###########################################################################################
    ###########################################################################################

    def __init__ (self, *args, **kwargs):

        super (CORE_TEST, self).__init__ (*args, **kwargs)

        self.USER_ID = 2
        self.ACCOUNT0_ID = 1
        self.ACCOUNT1_ID = 2

    ###########################################################################################
    ###########################################################################################

    def assertExists (self, object_id, manager):

        object = manager.get (id = object_id)
        self.assertFalse (object.deleted)

        return object

    def assertSoftDeleted (self, object, manager):

        object = object.reload (manager)
        self.assertTrue (object.deleted)

    def assertHardDeleted (self, object, manager):

        objects = manager.filter (pk = object.pk)
        self.assertTrue (len (objects) == 0)

    ###########################################################################################
    ###########################################################################################

    def test_soft_delete (self):

        user = self.assertExists (self.USER_ID, USER.objects)
        account0 = self.assertExists (self.ACCOUNT0_ID, ACCOUNT.objects)
        account1 = self.assertExists (self.ACCOUNT1_ID, ACCOUNT.objects)

        user.delete () ## soft delete

        self.assertSoftDeleted (user, USER.objects)
        self.assertSoftDeleted (account0, ACCOUNT.objects)
        self.assertSoftDeleted (account1, ACCOUNT.objects)

    def test_hard_delete (self):

        user = self.assertExists (self.USER_ID, USER.objects)
        account0 = self.assertExists (self.ACCOUNT0_ID, ACCOUNT.objects)
        account1 = self.assertExists (self.ACCOUNT1_ID, ACCOUNT.objects)

        user.delete (hard = True) ## hard delete

        self.assertHardDeleted (user, USER.objects)
        self.assertHardDeleted (account0, ACCOUNT.objects)
        self.assertHardDeleted (account1, ACCOUNT.objects)

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
