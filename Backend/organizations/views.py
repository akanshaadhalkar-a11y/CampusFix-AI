from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OrganizationSerializer
from .services import create_organization


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
