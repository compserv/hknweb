from django import forms

from hknweb.exams.models import Exam


class ExamUploadForm(forms.ModelForm):


    class Meta:
        model = Exam
        fields = ('department', 'course')
                  #'markdown', 'event_type', 'view_permission', 'rsvp_type', 'transportation')

        # help_texts = {
        #     'start_time': 'mm/dd/yyyy hh:mm, 24-hour time',
        #     'end_time': 'mm/dd/yyyy hh:mm, 24-hour time',
        #     'slug': 'e.g. <semester>-<name>',
        # }
        #
        # labels = {
        #     'slug': 'URL-friendly name',
        #     'rsvp_limit': 'RSVP limit',
        # }
