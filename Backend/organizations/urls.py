from django.urls import path

from .views import CreateOrganizationAPIView


urlpatterns = [
    path(
        "",
        CreateOrganizationAPIView.as_view(),
        name="create-organization",
    ),
]