from django.contrib.auth.models import User
from django.db import models

from hknweb.candidate.models.requirements.payment.due_payment import DuePayment


class DuePaymentPaidEntry(models.Model):
    users = models.ManyToManyField(User, blank=True)
    duePayment = models.OneToOneField(DuePayment, on_delete=models.CASCADE, unique=True)
    notes = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Due Payment Paid Entries"

    def __str__(self):
        return "Payments for: {}".format(self.duePayment)
