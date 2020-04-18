from django.http import HttpResponseRedirect
from django.shortcuts import render

from hknweb.exams.forms import ExamUploadForm
from .models import Course, Department, Instructor, Semester

def index(request):
	courses = Course.objects.order_by('name')

	context = {
		'courses': courses
	}

	return render(request, 'exams/index.html', context)

def exams_for_course(request, department, number):
	department = Department.objects.filter(name__exact=department).get()
	course = Course.objects.filter(department__exact=department.id).filter(number__exact=number).get()
	semesters = Semester.objects.filter(semester__exact=course.id)
	# CourseSemester.objects.filter(course__exact=course.id)


	context = {
		'course': course,
		'semesters': semesters
	}

	return render(request, 'exams/exams-course.html', context)


def add_exam(request):
	if request.method == 'POST':
		form = ExamUploadForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')

	return render(request, 'exams/exams_add.html', {'form': ExamUploadForm(None)})