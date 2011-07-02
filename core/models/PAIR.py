#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 30, 2011 3:20:01 PM$"

###############################################################################
###############################################################################

from django.db import models

###############################################################################
###############################################################################

class PAIR (models.Model):

    """
    An PAIR object represents a pair of ISO currency symbols.
    """

    class Meta:

        app_label = 'core'
        verbose_name_plural = 'pairs'

    ###########################################################################
    def __init__ (self, *args, **kwargs):
    ###########################################################################

        super (PAIR, self).__init__ (*args, **kwargs)

    ###########################################################################
    ###########################################################################

    quote = models.CharField (max_length=3, blank=True)
    base = models.CharField (max_length=3, blank=True)
    active = models.BooleanField (default=False)

    ###########################################################################
    ###########################################################################

    inverse = property (
        lambda self: PAIR (quote = self.base, base = self.quote)
    )

    def get_halted (self):

        return not self.active

    def set_halted (self, value):

        self.active = not value

    halted = property (get_halted, set_halted)

    ###########################################################################
    def __unicode__ (self):
    ###########################################################################

        return "%s/%s" % (self.quote, self.base)

###############################################################################
###############################################################################

class WRAP:

    def invoke (cls, method, *args):

        return getattr (WRAP, method)(cls, method, *args)

    invoke = staticmethod (invoke)

    def get_halted (cls, method, quote, base):

        pair = PAIR.objects.get (quote = quote, base = base)

        return '%s|%s|%s|%s|%s' % (cls, method, quote, base,
            pair.get_halted ()
        )

    get_halted = staticmethod (get_halted)

###############################################################################
###############################################################################

PAIR.invoke = staticmethod (WRAP.invoke)

###############################################################################
###############################################################################

if __name__ == "__main__":

    pass
