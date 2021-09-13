from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone


class Link(models.Model):
    class Meta:
        verbose_name_plural = "Links"  # fix plural without using Meta class

    name = models.CharField(max_length=255, null=False, unique=True)
    redirect = models.URLField()
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    last_accessed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.link_modified(["name", "redirect", "active"]):
            self.modified_at = django.utils.timezone.now()
        super().save(*args, **kwargs)  # Call the "real" save() method.

    def access_time_now(self):
        self.last_accessed_at = django.utils.timezone.now()
        self.save()

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._state.adding = False
        instance._state.db = db
        instance._old_values = dict(zip(field_names, values))
        return instance

    def link_modified(self, fields):
        if hasattr(self, "_old_values"):
            if not self.pk or not self._old_values:
                return True

            for field in fields:
                if getattr(self, field) != self._old_values[field]:
                    return True
            return False

        return True
