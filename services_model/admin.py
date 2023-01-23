from django.contrib import admin


class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}