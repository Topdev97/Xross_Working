from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="employees"),
    path("<id>", info, name="employee_info")
]
