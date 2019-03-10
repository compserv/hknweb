from django.shortcuts import render

from .models import Course, CourseSemester

def index(request):
	courses = Course.objects.order_by('name')

	context = {
		'courses': courses
	}

	return render(request, 'exams/index.html', context)

def exams_for_course(request, department, number):
	course = Course.objects.filter(department__exact=department).filter(number__exact=number).get()
	semesters = CourseSemester.objects.filter(course__exact=course.id)

	context = {
		'course': course,
		'semesters': semesters
	}

	return render(request, 'exams/exams-course.html', context)