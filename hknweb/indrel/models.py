from django.db import models

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length = 200)
    address_1 = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zipcode = models.IntegerField()
    contact_name = models.CharField(max_length = 200)
    contact_title = models.CharField(max_length = 200)
    contact_phone = models.CharField(max_length = 200)
    contact_email = models.EmailField()

    def __str__(self):
        return str(self.company_name)

    def __repr__(self):
        return ''.join(str(self.company_name).split()).lower()

class ResumeBookOrderForm(Company):
    comments = models.CharField(max_length = 5000)

class InfosessionRegistration(Company):
    preferred_week = models.CharField(max_length = 5000)
    preferred_food = models.CharField(max_length = 5000)
    advertisements = models.CharField(max_length = 5000)
    comments = models.CharField(max_length = 5000)
