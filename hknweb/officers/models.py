from django.db import models


class Committee(models.Model):
    id = models.AutoField(primary_key=True)
    short = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    is_exec = models.BooleanField(default=False)

    def __repr__(self):
        return 'Committee(short={}, name={})'.format(self.short, self.name)

    def __str__(self):
        return self.name


class Officer (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255, default='')
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
