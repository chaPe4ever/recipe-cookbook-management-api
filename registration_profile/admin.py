from django.contrib import admin

from registration_profile.models import RegistrationProfile


@admin.register(RegistrationProfile)
class RegistrationProfileAdmin(admin.ModelAdmin):
    pass
