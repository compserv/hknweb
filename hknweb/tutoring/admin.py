from django.contrib import admin

from .models import Course, TimeSlot, Slot, Tutor
from django.contrib.admin.views.main import ChangeList

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ['name']
	list_filter = ['name']
	search_fields = ['name']

@admin.register(TimeSlot)
class SlotAdmin(admin.ModelAdmin):
	list_display = ['day', 'hour']
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
	
	    