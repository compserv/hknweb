from django.db import models
from django.conf import settings
from hknweb.coursesemester.models import Semester


class BitByteGroup(models.Model):
    """
    Model for bit byte group.
    Each bit byte group has a semester associated with it, if it is unknown the field is none.
    """

    class Meta:
        verbose_name = "Bit Byte Group"
        verbose_name_plural = "Bit Byte Groups"

    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="bit_byte_groups",
    )

    bytes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bitbyte_groups_as_byte")
    bits = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="bitbyte_groups_as_bit")

    def __str__(self):
        return (
            f"Bit byte group {self.semester}; "
            + f"Bytes: {', '.join([c.username for c in self.bytes.all()])}; "
            + f"Bits: {', '.join([c.username for c in self.bits.all()])}"
        )
