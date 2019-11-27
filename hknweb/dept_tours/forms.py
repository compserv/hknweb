from django import forms

from .models import DepartmentTourRequest

class DepartmentTourForm(forms.ModelForm):

	class Meta:
		model = DepartmentTourRequest
		fields = ['name', 'tour_date', 'email', 'phone', 'comments']

	def __init__(self, *args, **kwargs):
		super(DepartmentTourForm, self).__init__(*args, **kwargs)
		self.fields['tour_date'].input_formats = [ '%m/%d/%Y %I:%M %p' ]