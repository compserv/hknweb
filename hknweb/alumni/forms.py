from django import forms
from hknweb.models import User
from hknweb.models import Profile
from .models import Alumnus

class AlumniForm(forms.ModelForm):

    class Meta:
        model = Alumnus
        fields = ('name_id','first_name','last_name','perm_email','mailing_list','grad_semester','grad_school','job_title','company','salary','location','suggestions')

