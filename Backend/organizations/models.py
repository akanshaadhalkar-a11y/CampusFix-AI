from django.conf import settings
from django.db import models
import secrets
import string


class Organization(models.Model):

    ORGANIZATION_TYPES = [
        ("COLLEGE", "College"),
        ("SCHOOL", "School"),
        ("OFFICE", "Office"),
        ("COMMUNITY", "Residential Community"),
    ]

    name = models.CharField(max_length=200)

    organization_type = models.CharField(
        max_length=20,
        choices=ORGANIZATION_TYPES
    )

    code = models.CharField(
        max_length=20,
        unique=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_organizations"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

class Membership(models.Model):

    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("STAFF", "Maintenance Staff"),
        ("MEMBER", "Member"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="MEMBER"
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"],
                name="unique_user_organization"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.organization} ({self.role})"