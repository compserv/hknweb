from django.contrib import admin

from .models import Course, Slot, Tutor
from .forms import SlotForm, TutorForm
from django.contrib.admin.views.main import ChangeList

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ['name']
	list_filter = ['name']
	search_fields = ['name']

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
	filter_horizontal = ('tutors',)
	list_display = ['day', 'hour', 'room']
	list_filter = ['room', 'day', 'hour', 'tutors']
	search_fields = ['room', 'day', 'hour', 'tutors']

@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
	filter_horizontal = ('courses',)
	list_display = ['name']
	list_filter = ['name', 'courses']
	search_fields = ['name', 'courses']
	
	    