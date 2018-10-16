from django.db import models


class Officer (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    imange = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    department = models.CharField(max_length=255, default='')
    personal_email = models.CharField(max_length=255)

    def __str__(self):
        return 'Officer(name = {} , title{}'.format(self.name, self.title)
