from django.contrib import admin

from accounts.models import Account


# Register your models here.
# admin.site.register(Account)

@admin.register(Account)
class AluminiAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_display_links = ['name', 'created_at']