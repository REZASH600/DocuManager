from django.contrib import admin

from apps.participants.models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "status")
    search_fields = ("first_name", "last_name")
    list_filter = ["status"]
