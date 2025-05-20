from django.urls import path
from orders.views import (
    BootcampRegisterPublicView,
    ListCaragoryBootcampView,
    DetailBootcmapView,
    ListRegisteredBootcampView,
    AdminCreateBootcampView,
    AdminDeleteBootcampView,
    AdminUpdateBootcampView,
    AdminCreateCatagoryView,
    AdminEditCatagoryView,
    AdminDeleteCatagoryView,
    ApproveBootcampRegistrationView,
)

urlpatterns = [
    path(
        "bootcamps/register-request/",
        BootcampRegisterPublicView.as_view(),
        name="bootcamp-register-request",
    ),
    path(
        "bootcamps/categories/",
        ListCaragoryBootcampView.as_view(),
        name="list-bootcamp-categories",
    ),
    path("bootcamps/<int:pk>/", DetailBootcmapView.as_view(), name="bootcamp-detail"),
    # Student View
    path(
        "bootcamps/registered/",
        ListRegisteredBootcampView.as_view(),
        name="list-registered-bootcamps",
    ),
    #  Admin & Register Support (Bootcamp CRUD)
    path(
        "admin/bootcamps/create/",
        AdminCreateBootcampView.as_view(),
        name="admin-create-bootcamp",
    ),
    path(
        "admin/bootcamps/<int:pk>/delete/",
        AdminDeleteBootcampView.as_view(),
        name="admin-delete-bootcamp",
    ),
    path(
        "admin/bootcamps/<int:pk>/update/",
        AdminUpdateBootcampView.as_view(),
        name="admin-update-bootcamp",
    ),
    # Admin & Register Support (Category CRUD)
    path(
        "admin/categories/create/",
        AdminCreateCatagoryView.as_view(),
        name="admin-create-category",
    ),
    path(
        "admin/categories/<int:pk>/update/",
        AdminEditCatagoryView.as_view(),
        name="admin-update-category",
    ),
    path(
        "admin/categories/<int:pk>/delete/",
        AdminDeleteCatagoryView.as_view(),
        name="admin-delete-category",
    ),
    #  Register Support (Approve Registration Request)
    path(
        "bootcamps/requests/<int:registration_id>/approve/",
        ApproveBootcampRegistrationView.as_view(),
        name="approve-registration",
    ),
]
