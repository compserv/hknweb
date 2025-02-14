from django.core.management.base import BaseCommand, CommandError

from hknweb.indrel.models import Resume

class Command(BaseCommand):
    help = "Generate Resume objects and the current Resume Book"
    
    def handle(self, **options):
        resumes = Resume.objects.all()
        for profile in resumes:
            user = profile.user
            if user.is_active:
                entry = Resume()
                