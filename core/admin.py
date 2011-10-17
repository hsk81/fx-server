from django.contrib import admin
from core.models import *

###############################################################################################
###############################################################################################

admin.site.register (STAMP)
admin.site.register (ADDRESS)
admin.site.register (ACCOUNT)
admin.site.register (SESSION)
admin.site.register (LIMIT_ORDER)
admin.site.register (MARKET_ORDER)
admin.site.register (STOP_LOSS_ORDER)
admin.site.register (TAKE_PROFIT_ORDER)
admin.site.register (RATE_TABLE)
admin.site.register (CLIENT)

###############################################################################################
###############################################################################################

class USERAdmin (admin.ModelAdmin):

    list_display = (
        'id', 'first_name', 'last_name', 'username', 'last_login', 'is_active'
    )

admin.site.register (USER, USERAdmin)

class PAIRAdmin (admin.ModelAdmin):

    list_display = ('id','quote','base', 'active')

admin.site.register (PAIR, PAIRAdmin)

class TICKAdmin (admin.ModelAdmin):

    list_display = ('id', 'get_date', 'get_time', 'ask', 'bid', 'pair')
    list_filter = ['datetime','pair']
    date_hierarchy = 'datetime'
    time_hierarchy = 'datetime'
    search_fields = ['datetime','ask','bid']

admin.site.register (TICK, TICKAdmin)

###############################################################################################
###############################################################################################
