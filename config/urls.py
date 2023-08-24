from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # path("admin_root/", admin.site.urls),
    path("admin/", include("customAdmin.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
    path("employers/", include("employer.urls")),
    path("employees/", include("employee.urls")),
    path("jobs/", include("job.urls")),
    path("proposals/", include("proposal.urls")),
    path("messages/", include("message.urls")),
    path("", include("bizxross.urls")),
]
