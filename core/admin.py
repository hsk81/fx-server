#! /usr/bin/python

__author__ = "hsk81"
__date__ = "$Apr 17, 2011 10:24:31 PM$"

###############################################################################################
###############################################################################################

from base.admin import *
from core.models import *
from django.contrib import admin

###############################################################################################
###############################################################################################

admin.site.register (ADDRESS)
admin.site.register (SESSION)
admin.site.register (LIMIT_ORDER)
admin.site.register (MARKET_ORDER)
admin.site.register (STOP_LOSS_ORDER)
admin.site.register (TAKE_PROFIT_ORDER)

###############################################################################################
###############################################################################################

class USER_ADMIN (BASE_ADMIN):

    list_display = ('id',
        'first_name', 'last_name', 'username', 'last_login', 'delete_date'
    )

    search_fields = ['id',
        'first_name', 'last_name', 'username', 'last_login', 'delete_date'
    ]

    list_filter = ['is_active', 'last_login', 'delete_date']
    
admin.site.register (USER, USER_ADMIN)

class ACCOUNT_ADMIN (BASE_ADMIN):

    list_display = ('id',
        'name', 'user', 'balance', 'home_currency', 'margin_rate', 'delete_date'
    )

    search_fields = ['id',
        'name', 'user__username', 'balance', 'home_currency', 'margin_rate', 'delete_date'
    ]
    
    list_filter = [
        'home_currency', 'margin_rate', 'delete_date'
    ]

admin.site.register (ACCOUNT, ACCOUNT_ADMIN)

class PAIR_ADMIN (BASE_ADMIN):

    list_display = ('id', 'quote', 'base', 'active')
    search_fields = ['id','quote', 'base', 'active']
    list_filter = ['quote', 'base', 'active']

admin.site.register (PAIR, PAIR_ADMIN)

class TICK_ADMIN (BASE_ADMIN):

    list_display = ('id', 'get_date', 'get_time', 'ask', 'bid', 'pair')
    search_fields = ['id','datetime', 'ask', 'bid']
    list_filter = ['datetime', 'pair']
    date_hierarchy = 'datetime'
    time_hierarchy = 'datetime'

admin.site.register (TICK, TICK_ADMIN)

###############################################################################################
###############################################################################################
