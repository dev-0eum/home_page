from django.contrib import admin

from accounts.models import Alumini

# Register your models here.
# admin.site.register(Account)

@admin.register(Alumini)
class AluminiAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_display_links = ['name', 'created_at']