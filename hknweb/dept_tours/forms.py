from django import forms
from django.utils.translation import ugettext as _

from .models import DepartmentTourRequest

class DepartmentTourForm(forms.ModelForm):

	verify_email = forms.EmailField(label="Verify Email")

	class Meta:
		model = DepartmentTourRequest
		fields = ['name', 'tour_date', 'email', 'verify_email', 'phone', 'comments']

	def __init__(self, *args, **kwargs):
		super(DepartmentTourForm, self).__init__(*args, **kwargs)
		self.fields['tour_date'].input_formats = [ '%m/%d/%Y %I:%M %p' ]

	def clean_verify_email(self):
		second_email = self.cleaned_data['verify_email']
		first_email = self.cleaned_data['email']
		if second_email != first_email:
			raise forms.ValidationError(_('Invalid email: "%(second)s" does not match "%(first)s"'),
											code='emails_not_matching', params={'first': first_email, 'second': second_email})
