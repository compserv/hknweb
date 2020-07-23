from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from django.core.validators import RegexValidator
from django.utils import timezone

MAX_STRLEN = 85 # default max length for char fields
MAX_TXTLEN = 2000 # default max length for text fields

# Pretty sure this is terrible coding practice but hey it works
# Sorry Daddy DeNero
User.__str__ = lambda self: "{} ({} {})".format(self.username, self.first_name, self.last_name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    date_of_birth = models.DateField(null=True, blank=True)
    picture = models.ImageField(blank=True)
    private = models.BooleanField(default=True, verbose_name="Private profile?")
    phone_regex = RegexValidator(regex=r'^/([^\d]*\d){10}$/', message="Phone number must be ten digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    resume = models.FileField(blank=True)
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

class Announcement(models.Model):
    """
    Model for an announcement. Created by VP or some other superuser.
    Displayed on the candidate portal. The title will be displayed in bold,
    and the text will follow that in normal font, with a space in between.
    """

    title           = models.CharField(max_length=MAX_STRLEN, default='')
    text            = models.TextField(max_length=MAX_TXTLEN, blank=True, default='')
    # if visible == False, then admins can see announcement but it's not displayed on portal
    visible         = models.BooleanField(default=False)
    release_date    = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title if self.title != '' else self.text
