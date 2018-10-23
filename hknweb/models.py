from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='public/images/profile/')
    private = models.BooleanField(default=True, verbose_name="Private profile?")
    phone_regex = RegexValidator(regex=r'^([^\d]*\d){10}$', message="Phone number must be ten digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    resume = models.FileField(blank=True, upload_to='private/resumes/')
    graduation_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def clean(self):
        if self.phone_number:
            self.phone_number = re.sub("[^0-9]", "",self.phone_number)
            self.phone_number = "("+self.phone_number[0:3]+") "+self.phone_number[3:6]+"-"+self.phone_number[6:]
