from django.contrib import admin

from hknweb.tutoring.models import Tutor, Room, TutoringLogistics, Slot


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")
    autocomplete_fields = ('user',)


@admin.register(TutoringLogistics)
class TutoringLogisticsAdmin(admin.ModelAdmin):
    autocomplete_fields = ("one_hour_tutors", "two_hour_tutors")


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    autocomplete_fields = ("tutors",)


admin.site.register(Room)
