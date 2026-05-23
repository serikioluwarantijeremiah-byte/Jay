from django.contrib import admin
from .models import Store, SyncLog

admin.site.register(Store)
admin.site.register(SyncLog)