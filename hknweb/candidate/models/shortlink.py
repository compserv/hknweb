from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class ShortLink(models.Model):
    """
    Model for URL shortlinks (e.g., hkn.mu/discord -> https://discord.gg/xyz)
    """

    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9-_]+$",
                message="Slug can only contain letters, numbers, hyphens, and underscores",
            )
        ],
        help_text="Short code for the URL (e.g., 'discord', 'apply')",
    )
    destination_url = models.URLField(
        max_length=2000, help_text="Full URL to redirect to"
    )
    description = models.CharField(
        max_length=500, blank=True, help_text="Optional description for officers"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_shortlinks",
        help_text="Officer who created this shortlink",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    click_count = models.PositiveIntegerField(
        default=0, help_text="Number of times this shortlink has been used"
    )
    active = models.BooleanField(
        default=True, help_text="Whether this shortlink is active"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Short Link"
        verbose_name_plural = "Short Links"

    def __str__(self):
        return f"{self.slug} -> {self.destination_url}"

    def increment_click_count(self):
        """Increment the click counter atomically"""
        self.click_count = models.F("click_count") + 1
        self.save(update_fields=["click_count"])
