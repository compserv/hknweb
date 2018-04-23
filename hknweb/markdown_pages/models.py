from django.db import models
from markdownx.models import MarkdownxField

class MarkdownPage(models.Model):
    id          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=255, null=False)
    path        = models.CharField(max_length=255, db_index=True, unique=True)
    description = models.CharField(max_length=255)
    body        = MarkdownxField()

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "MarkdownPage(name={}, path={})".format(self.name, self.path)
