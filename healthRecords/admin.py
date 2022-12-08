from django.contrib import admin

from .models import HealthRecord, HealthRecordFolder

class FolderAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")

class RecordAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")

admin.site.register(HealthRecord, FolderAdmin)
admin.site.register(HealthRecordFolder, RecordAdmin)