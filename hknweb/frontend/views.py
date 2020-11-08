from django.views.generic import TemplateView


class DepartmentsView(TemplateView):
    template_name = 'frontend/departments.html'


class InstructorsView(TemplateView):
    template_name = 'frontend/instructors.html'
