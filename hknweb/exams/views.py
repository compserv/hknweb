from django.http import HttpResponseRedirect
from django.shortcuts import render

from hknweb.exams.forms import ExamUploadForm
from .models import Course, Department, Instructor, Semester, CourseSemester

def index(request):
	courses = Course.objects.order_by('name')

	context = {
		'courses': courses,
		'searchCourses': CourseSemester.objects.all()
	}

	return render(request, 'exams/index.html', context)

def exams_for_course(request, department, number):

	department = Department.objects.filter(abbreviated_name__exact=department).get()
	course = Course.objects.filter(department__exact=department.id).filter(number__exact=number).get()
	semesters = CourseSemester.objects.filter(course__exact=course.id)

	# print(semesters)

	context = {
		'course': course,
		'semesters': semesters
	}

	return render(request, 'exams/exams-course.html', context)


def add_exam(request):
	if request.method == 'POST':
		form = ExamUploadForm(request.POST, request.FILES)
		if form.is_valid():
			semester = form.cleaned_data['semester']
			course = form.cleaned_data['course']
			exam = form.cleaned_data['exam']
			type = form.cleaned_data['type']

			courseSemester = CourseSemester.objects.filter(course=course, semester=semester).first()

			# print(courseSemester)
			# print(exam + type)

			setattr(courseSemester, exam + ('_sol' if (type == 'sol') else ''), request.FILES['file'])
			courseSemester.save()

			return HttpResponseRedirect('/')
		else:
			print(form.errors)

	return render(request, 'exams/exams_add.html', {'form': ExamUploadForm(None)})