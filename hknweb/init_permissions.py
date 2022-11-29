from hknweb.candidate.models import Announcement, OffChallenge, BitByteActivity
from hknweb.events.models import Event, Rsvp, AttendanceForm
from hknweb.academics.models import AcademicEntity
from hknweb.markdown_pages.models import MarkdownPage
from hknweb.tutoring.models import Slot

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


def provision():
    candidate, _ = Group.objects.get_or_create(name="candidate")
    officer, _ = Group.objects.get_or_create(name="officer")

    # CANDIDATE AND OFFICER PERMISSIONS
    cand_permission_names = [
        ("view_announcement", Announcement),
        ("add_offchallenge", OffChallenge),
        ("view_offchallenge", OffChallenge),
        ("change_offchallenge", OffChallenge),
        ("add_bitbyteactivity", BitByteActivity),
        ("add_rsvp", Rsvp),
        ("view_rsvp", Rsvp),
        ("change_rsvp", Rsvp),
        ("delete_rsvp", Rsvp),
        ("view_user", User),
        ("view_event", Event),
    ]

    # OFFICER ONLY PERMISSIONS
    off_permission_names = [
        ("add_event", Event),
        ("change_event", Event),
        ("delete_event", Event),
        ("add_academicentity", AcademicEntity),
        ("view_academicentity", AcademicEntity),
        ("change_academicentity", AcademicEntity),
        ("add_attendanceform", AttendanceForm),
        ("add_markdownpage", MarkdownPage),
        ("add_user", User),
        ("add_slot", Slot),
    ]

    # SETTING PERMISSIONS TO GROUPS
    for codename, model in cand_permission_names:
        ct = ContentType.objects.get_for_model(model)
        permission = Permission.objects.get(codename=codename, content_type=ct)
        candidate.permissions.add(permission)
        officer.permissions.add(permission)

    for codename, model in off_permission_names:
        ct = ContentType.objects.get_for_model(model)
        permission = Permission.objects.get(codename=codename, content_type=ct)
        officer.permissions.add(permission)
