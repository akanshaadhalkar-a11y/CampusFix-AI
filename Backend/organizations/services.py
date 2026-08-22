import secrets
import string
import re
from django.db import transaction


def generate_organization_code(prefix="ORG"):

    """
    Generate a unique organization code.

    Example:
    ORG-7K4P9X
    """

    characters = string.ascii_uppercase + string.digits

    while True:
        random_part = "".join(
            secrets.choice(characters)
            for _ in range(6)
        )

        code = f"{prefix}-{random_part}"

        from .models import Organization

        if not Organization.objects.filter(code=code).exists():
            return code

def validate_custom_organization_code(code):

    """
    Validate a custom organization code.

    Rules:
    - 4 to 20 characters
    - Uppercase letters, numbers, and hyphens only
    - Must be unique
    """

    code = code.strip().upper()

    if not 4 <= len(code) <= 20:
        return False, "Code must be between 4 and 20 characters."

    if not re.fullmatch(r"[A-Z0-9-]+", code):
        return False, "Code can contain only letters, numbers, and hyphens."

    from .models import Organization

    if Organization.objects.filter(code=code).exists():
        return False, "This organization code is already in use."

    return True, code

@transaction.atomic
def create_organization(

    *,
    user,
    name,
    organization_type,
    location="",
    code=None,
    generate_code=True,
):
    """
    Create an organization and make the creator its admin.
    """

    from .models import Organization, Membership

    if generate_code:
        code = generate_organization_code()
    else:
        is_valid, result = validate_custom_organization_code(code)

        if not is_valid:
            raise ValueError(result)

        code = result

    organization = Organization.objects.create(
        name=name.strip(),
        organization_type=organization_type,
        location=location.strip(),
        code=code,
        created_by=user,
    )

    Membership.objects.create(
        user=user,
        organization=organization,
        role="ADMIN",
    )

    return organization

@transaction.atomic
def join_organization(*, user, code):

    from .models import Organization, Membership

    code = code.strip().upper()

    try:
        organization = Organization.objects.get(code=code)
    except Organization.DoesNotExist:
        raise ValueError("Organization with this code does not exist.")

    if Membership.objects.filter(
        user=user,
        organization=organization
    ).exists():
        raise ValueError("You are already a member of this organization.")

    membership = Membership.objects.create(
        user=user,
        organization=organization,
        role="MEMBER",
    )

    return membership

@transaction.atomic
def change_member_role(*, admin_user, membership_id, new_role):
    from .models import Membership

    try:
        admin_membership = Membership.objects.get(
            user=admin_user,
            role="ADMIN",
        )
    except Membership.DoesNotExist:
        raise ValueError(
            "Only organization admins can change member roles."
        )

    try:
        membership = Membership.objects.select_related(
            "organization",
            "user",
        ).get(id=membership_id)
    except Membership.DoesNotExist:
        raise ValueError("Membership does not exist.")

    if membership.organization_id != admin_membership.organization_id:
        raise ValueError(
            "You cannot manage members from another organization."
        )

    if membership.user_id == admin_user.id:
        raise ValueError(
            "You cannot change your own role."
        )

    membership.role = new_role
    membership.save(update_fields=["role"])

    return membership