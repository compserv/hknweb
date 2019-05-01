from django.shortcuts import render

from .models import Course, CourseSemester, Department, Instructor

def index(request):
	courses = Course.objects.order_by('name')

	context = {
		'courses': courses
	}

	return render(request, 'exams/index.html', context)

def exams_for_course(request, department, number):
	department = Department.objects.filter(name__exact=department).get()
	course = Course.objects.filter(department__exact=department.id).filter(number__exact=number).get()
	semesters = CourseSemester.objects.filter(course__exact=course.id)

	context = {
		'course': course,
		'semesters': semesters
	}

	return render(request, 'exams/exams-course.html', context)