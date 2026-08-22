from rest_framework import serializers

from .models import Organization


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