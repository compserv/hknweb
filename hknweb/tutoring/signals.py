from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from hknweb import settings
from hknweb.models import Committeeship, User
from hknweb.tutoring.models import Tutor


@receiver(m2m_changed, sender=Committeeship.committee_members.through)
def deleteTutorIfRemovedFromCommittee(sender, instance, action, pk_set, **_):
    if action == "post_remove":
        Tutor.objects.filter(user__pk__in=pk_set).exclude(
            user__pk__in=User.objects.filter(
                pk__in=pk_set, cmembership__committee=settings.TUTORING_GROUP
            ).values_list("pk", flat=True)
        ).delete()
