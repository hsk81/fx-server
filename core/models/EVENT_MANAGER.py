#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 28, 2011 5:05:58 PM$"

###############################################################################
###############################################################################

from uuid import uuid4 as uuid
from django.db import models
from core.models import *

###############################################################################
###############################################################################

## public abstract class FXEventManager extends java.lang.Object
class EVENT_MANAGER (models.Model):

    """
    The EVENT_MANAGER class keeps track of a set of EVENTs of a particular type,
    handling their registration, notification, and deregistration.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'event managers'

    def __init__ (self, *args, **kwargs):

        super (EVENT_MANAGER, self).__init__ (*args, **kwargs)

        self.uuid = uuid ()
        self.events = []

    ##  boolean add(FXEvent e)
    def add (self, event):
        """
        Add an EVENT to this EVENT_MANAGER, to be notified of incoming
        EVENT_INFOs.
        """
        self.events.append (event)

    ##  java.util.Vector getEvents()
    def get_events (self):
        """
        Gets the list of events currently registered to this EVENT_MANAGER.
        """
        return self.events
    
    ##  boolean remove(FXEvent e)
    def remove (self, event):
        """
        Remove an EVENT from this EVENT_MANAGER, denying further notifications.
        """
        self.events.remove (event)
        
    def __unicode__ (self):
        """
        Returns string representation for this EVENT_MANAGER.
        """
        return "%s" % self.uuid

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
