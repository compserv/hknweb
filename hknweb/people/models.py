from django.db import models

class People(models.Model):
    id                  = models.IntegerField(primary_key=True)
    first_name          = models.CharField(max_length=255, null=False)
    last_name           = models.CharField(max_length=255, null=False)
    username            = models.CharField(max_length=255, null=False)
    email               = models.CharField(max_length=255, null=False)
    phone_number        = models.CharField(max_length=255)
    date_of_birth       = models.DateField()
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    picture             = models.CharField(max_length=255)
    private             = models.BooleanField(default=True, null=False)
    local_address       = models.CharField(max_length=255, default="")
    perm_address        = models.CharField(max_length=255, default="")
    grad_semester       = models.CharField(max_length=255, default="")
    approved            = models.BooleanField()
    graduation          = models.CharField(max_length=255)



