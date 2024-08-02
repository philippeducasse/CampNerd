from django.contrib import admin
from .models import Buchung, ChangeLog

admin.site.register(Buchung)

@admin.register(ChangeLog)
class LogAdmin(admin.ModelAdmin):
    list_display = ('field_changed', 'old_value', 'new_value', 'date', 'user')
    list_filter = ('date', 'user')
    search_fields = ('field_changed', 'old_value', 'new_value', 'user__username')

