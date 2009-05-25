from django.contrib import admin
from models import *

class RefererInline(admin.TabularInline):
    model = Referer

admin.site.register(DownloadCounter,
    inlines = [
        RefererInline,
    ],
)

