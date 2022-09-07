from django.contrib import admin

from .models import (
    RoomPreference,
    TutorCourse,
    TimeSlot,
    Slot,
    Tutor,
    CoursePreference,
    Room,
    TimeSlotPreference,
)


@admin.register(TutorCourse)
class TutorCourseAdmin(admin.ModelAdmin):
    list_display = ["course"]
    list_filter = ["course"]
    search_fields = ["course"]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_filter = ["day", "hour"]
    search_fields = ["day", "hour"]
    actions = ["resync_timeslot_id", "reset_database_time_information"]

    def resync_timeslot_id(self, request, queryset):
        queryset_ordered = queryset.order_by("hour", "day")
        id_num = 0
        for timeslot_query in queryset_ordered:
            timeslot_query.timeslot_id = id_num
            timeslot_query.save()
            id_num += 1

    resync_timeslot_id.short_description = (
        "Resync Time Slot ID in order of time (hour then day)"
    )

    def reset_database_time_information(self, request, queryset):
        Room.objects.all().delete()
        Slot.objects.all().delete()
        TutorCourse.objects.all().delete()
        TimeSlot.objects.all().delete()
        TimeSlotPreference.objects.all().delete()
        RoomPreference.objects.all().delete()

    reset_database_time_information.short_description = "Reset the time slot information if e.g. the semester's offered tutoring hours change"


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ["timeslot", "room"]
    list_filter = ["room", "timeslot", "tutors"]
    search_fields = ["room", "timeslot", "tutors"]
    actions = ["resync_slot_id"]

    def resync_slot_id(self, request, queryset):
        queryset_ordered = queryset.order_by(
            "timeslot__hour", "timeslot__day", "room__id"
        )
        slot_id = 0
        for slot_query in queryset_ordered:
            slot_query.slot_id = slot_id
            slot_id += 1
            slot_query.save()

    resync_slot_id.short_description = "Resync Slot ID in order of time (hour then day)"


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(CoursePreference)
class CoursePreferenceAdmin(admin.ModelAdmin):
    list_display = ["tutor", "course", "preference"]
    list_filter = ["tutor", "course", "preference"]
    search_fields = ["tutor", "course", "preference"]


@admin.register(TimeSlotPreference)
class TimeSlotPreferenceAdmin(admin.ModelAdmin):
    list_display = ["tutor", "timeslot", "preference"]
    list_filter = ["tutor", "timeslot", "preference"]
    search_fields = ["tutor", "timeslot", "preference"]


@admin.register(RoomPreference)
class RoomPreferenceAdmin(admin.ModelAdmin):
    list_display = ["tutor", "timeslot", "room", "preference"]
    list_filter = ["tutor", "timeslot", "room", "preference"]
    search_fields = ["tutor", "timeslot", "room", "preference"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["building", "room_num"]
    list_filter = ["building"]
    search_fields = ["building", "room_num"]
