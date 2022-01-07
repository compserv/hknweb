from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from hknweb.academics.models import AcademicEntity
from hknweb.academics.tests.utils import ModelFactory

from hknweb.course_surveys.constants import COURSE_SURVEYS_EDIT_PERMISSION


def create_user_with_course_surveys_edit_permission(test):
    user = ModelFactory.create_user()
    password = "custom password"
    user.set_password(password)
    user.save()

    content_type = ContentType.objects.get_for_model(AcademicEntity)
    permission_str = COURSE_SURVEYS_EDIT_PERMISSION.split(".")[1]
    permission = Permission.objects.get(
        content_type=content_type,
        codename=permission_str,
    )
    user.user_permissions.add(permission)

    test.client.login(username=user.username, password=password)
