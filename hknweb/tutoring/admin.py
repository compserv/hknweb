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
	actions = ['resync_slot_id']

	def resync_slot_id(self, request, queryset):
		queryset_ordered = queryset.order_by('timeslot__day', 'timeslot__hour')
		id_num = 0
		for slot_query in queryset_ordered:
			slot_query.slot_id = id_num
			slot_query.timeslot.timeslot_id = id_num
			slot_query.timeslot.save()
			slot_query.save()
			id_num += 1
	
	resync_slot_id.short_description = "Resync Slot ID (and Time Slot) in order of time (day then hour)"

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
