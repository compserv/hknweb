from django.contrib import admin

from .models import TutorCourse, TimeSlot, Slot, Tutor, CoursePreference, \
	Room, TimeSlotPreference

@admin.register(TutorCourse)
class TutorCourseAdmin(admin.ModelAdmin):
	list_display = ['course']
	list_filter = ['course']
	search_fields = ['course']

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
	list_filter = ['day', 'hour']
	search_fields = ['day', 'hour']

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
	list_display = ['timeslot', 'room']
	list_filter = ['room', 'timeslot', 'tutors']
	search_fields = ['room', 'timeslot', 'tutors']

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
	list_display = ['name']
	list_filter = ['name']
	search_fields = ['name']
	
@admin.register(CoursePreference)
class CoursePreferenceAdmin(admin.ModelAdmin):
	list_display = ['tutor', 'course', 'preference']
	list_filter = ['tutor', 'course', 'preference']
	search_fields = ['tutor', 'course', 'preference']

@admin.register(TimeSlotPreference)
class TimeSlotPreferenceAdmin(admin.ModelAdmin):
	list_display = ['tutor', 'timeslot', 'time_preference','office_preference']
	list_filter = ['tutor', 'timeslot', 'time_preference','office_preference']
	search_fields = ['tutor', 'timeslot', 'time_preference','office_preference']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ['building', 'room_num']
	list_filter = ['building']
	search_fields = ['building', 'room_num']
