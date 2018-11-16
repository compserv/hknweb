from django.db import models

class Committee(models.Model):
    id = models.AutoField(primary_key=True)
    short = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    is_exec = models.BooleanField(default=False)

    @property
    def email(self):
        return "{}@hkn.eecs".format(self.short)

    def __repr__(self):
        return 'Committee(short={}, name={})'.format(self.short, self.name)

    def __str__(self):
        return self.name


class Officer(models.Model):
    profile = models.OneToOneField('hknweb.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)

    def __repr__(self):
        return 'Officer(name={}, title={}, committee={})'.format(
            self.name,
            self.title,
            self.committee,
        )

    def __str__(self):
        return self.name
