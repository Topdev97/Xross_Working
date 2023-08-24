from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="employers"),
    path("<id>", info, name="employer_info")
]
