from django.db import models


class Alumnus(models.Model):
    perm_email = models.EmailField()
    mailing_list = models.BooleanField()
    grad_semester = models.CharField()
    pub_date = models.DateTimeField('date published')

    def grad_semester(self, semester, year):
        return semester + ' ' + year

    was_published_recently.admin_order_field = 'pub_date'
        was_published_recently.boolean = True
        was_published_recently.short_description = 'Published recently?'

        def __str__(self):
            return self.question_text