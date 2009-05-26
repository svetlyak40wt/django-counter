from django.contrib import admin
from models import *

class RefererInline(admin.TabularInline):
    model = Referer

_list_display = ('id', 'title', 'url', 'count')
admin.site.register(RedirCounter,
    inlines = [
        RefererInline,
    ],
    list_display = _list_display,
    list_display_links = _list_display,
)

admin.site.register(Referer,
    list_display = ('id', 'counter', 'url', 'count', 'update_date'),
    date_hierarchy = 'update_date',
    list_filter = ('update_date',),
)

admin.site.register(ViewCounter,
    list_display = ('get_object_title', 'get_content_type', 'count'),
    list_filter = ('content_type',),
)

