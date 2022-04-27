from django.conf import settings

from django.db import models

# Create your models here.


class ThreadTask(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)
    message = models.TextField(blank=True)
    is_successful = models.BooleanField(blank=False, default=False)
    is_done = models.BooleanField(blank=False, default=False)

    def complete(self):
        self.is_successful = True
        self.is_done = True

    def failure(self, error_text=""):
        self.error_text = error_text
        self.is_successful = False
        self.is_done = True

    def startThread(self, thread):
        """
        Abstraction of starting a thread
        Main requirement is the "setDaemon" to be true
        alongside the "start" (of course)
        """
        if getattr(settings, "NO_THREADING", False):  # pragma: no cover
            thread._target(*thread._args)
            return

        thread.setDaemon(True)
        thread.start()
