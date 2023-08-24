from django.urls import path

from .views import *

urlpatterns = [
    path("employer/<job_id>", employer_messages, name="employer_messages"),
    path("employer/<job_id>/<user_id>", employer_message, name="employer_message"),
    path("employee", employee_messages, name="employee_messages"),
    path("employee/<job_id>", employee_message, name="employee_message"),
]
