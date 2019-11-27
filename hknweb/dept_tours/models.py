from django.db import models

MAX_STRLEN = 85 # Default maximum length for a char field
MAX_NUMLEN = 12 # Default maximum length for phone number field
MAX_TXTLEN = 2000 # default max length for text fields

class DepartmentTourRequest(models.Model):
	"""
	Model for site visitors to request a department tour
	"""

	# Name of person requesting the tour
	name = models.CharField(max_length=MAX_STRLEN, default='')
	# Date and time requested for tour
	tour_date = models.DateTimeField()
	# Email address to contact requester
	email = models.EmailField(max_length=MAX_STRLEN)
	# Phone number to contact requester
	phone = models.CharField(max_length=MAX_NUMLEN, default='')
	# Any addtional comments
	comments = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')

	def __str__(self):
		return self.name + ' @ ' + self.tour_date.strftime('%m/%d/%Y %I:%M %p')
