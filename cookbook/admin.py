from django.contrib import admin

from cookbook.models import Cookbook


@admin.register(Cookbook)
class CookbookAdmin(admin.ModelAdmin):
    pass
