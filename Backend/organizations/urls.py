from django.urls import path

from .views import CreateOrganizationAPIView,JoinOrganizationAPIView


urlpatterns = [
    path(
        "",
        CreateOrganizationAPIView.as_view(),
        name="create-organization",
    ),

     path(
        "join/",
        JoinOrganizationAPIView.as_view(),
        name="join-organization",
    ),
]