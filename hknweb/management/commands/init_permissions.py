from django.core.management.base import BaseCommand

from hknweb.init_permissions import provision


class Command(BaseCommand):
    help = "Provisions the database with default permissions data"

    def handle(self, **options):
        provision()
