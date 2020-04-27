from django.db import models
from django import forms
from django.core.mail import send_mail,EmailMessage
import json
class IndrelMailerUnderlying(models.Model):
    sender=models.CharField(default='indrel@hkn.eecs.berkeley.edu',max_length=200)
    receiver=models.CharField(max_length=200)
    conf_receiver=models.CharField(default='indrel@hkn.eecs.berkeley.edu',max_length=200)
    subject=models.CharField(max_length=200)
    template=models.FileField()
    fillins=models.FileField()

    class Meta:
        verbose_name = "Indrel Mailer Instance"

    def send_email(self):
        recs = self.receiver.split(",")
        template = self.template.read().decode('utf-8')

        try:
            fillins = json.loads(self.fillins.read().decode('utf-8'))
        except json.JSONDecodeError:
            print("JSON File was not in proper format")

        for rec in recs:
            rec_temp = template
            rec_subject = self.subject
            for field in fillins[rec]:
                rec_temp = rec_temp.replace("{" + str(field) + "}", str(fillins[rec][field]))
                rec_subject = rec_subject.replace("{" + str(field) + "}", str(fillins[rec][field]))
            result = send_mail(rec_subject, rec_temp, self.sender, [rec])
            if result == 0:
                print("Email to {} failed to send".format(rec))
        # return send_mail(self.cleaned_data['subject'],self.cleaned_data['mail'],self.cleaned_data['sender'],
        #           self.cleaned_data['receiver'].split(","))
class IndrelMailer(forms.ModelForm):
    class Meta:
        model=IndrelMailerUnderlying
        fields=['sender','receiver','conf_receiver','subject','template','fillins']
        labels={'conf_receiver':"Confirmation Receiver"}




class Company(models.Model):
    company_name = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.company_name)

    def __repr__(self):
        return ''.join(str(self.company_name).split()).lower()

class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    title = models.CharField(max_length = 200)
    phone = models.CharField(max_length = 200)
    email = models.EmailField()

class CompanyLocation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zipcode = models.IntegerField()

class ResumeBookOrderForm(models.Model):
    company = Company()
    comments = models.CharField(max_length = 5000)

class InfosessionRegistration(models.Model):
    company = Company()
    preferred_week = models.CharField(max_length = 5000)
    preferred_food = models.CharField(max_length = 5000)
    advertisements = models.CharField(max_length = 5000)
    comments = models.CharField(max_length = 5000)

class EventType(models.Model):
    event_type = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.event_type)

class Event(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length = 500)
    event_type = EventType()
    food = models.CharField(max_length = 5000)
    prizes = models.CharField(max_length = 5000)
    turnout = models.IntegerField()
    company = Company()
    contact = Contact()
    officer = models.CharField(max_length = 200)
    feedback = models.CharField(max_length = 5000)
    comments = models.CharField(max_length = 5000)
