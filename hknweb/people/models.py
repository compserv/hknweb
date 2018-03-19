from django.db import models

class People(models.Model):
    id                  = models.IntegerField(primary_key=True)
    first_name          = models.CharField(max_length=255, null=False)
    last_name           = models.CharField(max_length=255, null=False)
    username            = models.CharField(max_length=255, null=False)
    email               = models.CharField(max_length=255, null=False)
    crypted_password    = models.CharField(max_length=255, null=False)
    password_salt       = models.CharField(max_length=255, null=False)
    persistence_token   = models.CharField(max_length=255, null=False)
    single_access_token = models.CharField(max_length=255, null=False)
    perishable_token    = models.CharField(max_length=255, null=False)
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
    failed_login_count  = models.IntegerField(default=0, null=False)
    current_login_at    = models.DateTimeField()
    reset_password_link = models.CharField(max_length=255)
    reset_password_at   = models.DateTimeField()
    graduation          = models.CharField(max_length=255)



