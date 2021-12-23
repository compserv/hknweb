from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from hknweb.events.models import Rsvp

from hknweb.events.tests.models.utils import ModelFactory


def setUp(test, permission_names):
    user = ModelFactory.create_user()
    password = "custom password"
    user.set_password(password)
    user.save()

    content_type = ContentType.objects.get_for_model(Rsvp)
    for permission_name in permission_names:
        permission = Permission.objects.get(
            content_type=content_type, codename=permission_name
        )
        user.user_permissions.add(permission)

    test.client.login(username=user.username, password=password)

    event_type = ModelFactory.create_event_type()
    event = ModelFactory.create_event(
        name="custom event name",
        event_type=event_type,
        created_by=user,
        access_level=2,
    )

    test.user = user
    test.password = password
    test.event = event
