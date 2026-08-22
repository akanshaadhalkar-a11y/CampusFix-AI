from django.urls import path

from .views import CreateOrganizationAPIView,JoinOrganizationAPIView,OrganizationMembersAPIView,ChangeMemberRoleAPIView


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
    path(
        "members/",
        OrganizationMembersAPIView.as_view(),
        name="organization-members",
    ),

    path(
    "members/<int:membership_id>/role/",
    ChangeMemberRoleAPIView.as_view(),
    name="change-member-role",
    ),
]
