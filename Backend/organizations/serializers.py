from rest_framework import serializers

from .models import Organization,Membership


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "organization_type",
            "code",
            "location",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "code",
            "created_at",
        ]

class JoinOrganizationSerializer(serializers.Serializer):

    code = serializers.CharField(
        max_length=20,
        required=True
    )      

class MembershipSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Membership
        fields = [
            "id",
            "username",
            "email",
            "role",
            
        ]

class ChangeMemberRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=Membership.ROLE_CHOICES
    )        