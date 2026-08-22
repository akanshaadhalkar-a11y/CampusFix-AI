from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OrganizationSerializer,JoinOrganizationSerializer
from .services import create_organization , join_organization


class CreateOrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            organization = create_organization(
                user=request.user,
                name=serializer.validated_data["name"],
                organization_type=serializer.validated_data["organization_type"],
                location=serializer.validated_data.get("location", ""),
                code=request.data.get("code"),
                generate_code=request.data.get("generate_code", True),
            )
        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            OrganizationSerializer(organization).data,
            status=status.HTTP_201_CREATED,
        )
# Create your views here.
class JoinOrganizationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JoinOrganizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            membership = join_organization(
                user=request.user,
                code=serializer.validated_data["code"],
            )
        except ValueError as error:
            return Response(
                {"error": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
    {
        "message": "Successfully joined the organization.",
        "role": membership.role,
        "organization": {
            "id": membership.organization.id,
            "name": membership.organization.name,
            "code": membership.organization.code,
        },
    },
    status=status.HTTP_201_CREATED,
)