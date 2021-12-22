from django.contrib.auth.models import User
from django.db import models

from hknweb.candidate.models.requirements.payment.due_payment import DuePayment


class DuePaymentPaidEntry(models.Model):
    users = models.ManyToManyField(User)
    duePayment = models.OneToOneField(DuePayment, models.CASCADE)
    notes = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Due Payment Paid Entries"

    def __str__(self):
        return "Payments for: {}".format(self.duePayment)
