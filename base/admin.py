#! /usr/bin/python

__author__="hsk81"
__date__ ="$Oct 23, 2011 9:15:46 PM$"

###############################################################################################
###############################################################################################

from django.contrib import admin

###############################################################################################
###############################################################################################

class BASE_INLINE (admin.TabularInline): pass
class BASE_ADMIN (admin.ModelAdmin): pass

###############################################################################################
###############################################################################################

if __name__ == "__main__":

    pass
