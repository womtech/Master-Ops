from django.contrib import admin
from .models import Machine, Request, DownloadLog, CloudFile, StorageDevice, Nudge

# Register your models here.
admin.site.register([Machine, Request, DownloadLog, CloudFile, StorageDevice, Nudge])
