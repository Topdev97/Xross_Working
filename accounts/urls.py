from django.urls import path

from .views import *
import employee.views as employee
import employer.views as employer
import job.views  as job

urlpatterns = [
    path("register_info", register_info, name="accounts_register_info"),
    
    path("basic_info", accounts_basic_info, name="accounts_basic_info"),
    path("employee_profile", employee.accounts_profile, name="accounts_employee_profile"),
    path("employer_profile", employer.accounts_profile, name="accounts_employer_profile"),
    path("experience", employee.accounts_experience, name="accounts_experience"),
    path("experience/create", employee.accounts_experience_create, name="accounts_experience_create"),
    path("experience/update", employee.accounts_experience_update, name="accounts_experience_update"),
    path("experience/delete", employee.accounts_experience_delete, name="accounts_experience_delete"),
    path("skill", employee.accounts_skill, name="accounts_skill"),
    path("skill/create", employee.accounts_skill_create, name="accounts_skill_create"),
    path("skill/update", employee.accounts_skill_update, name="accounts_skill_update"),
    path("skill/delete", employee.accounts_skill_delete, name="accounts_skill_delete"),
    path("accounts_menu", accounts_menu, name="accounts_menu"),
    path("workspace/create", job.create, name="job_post"),
    path("email/change", accounts_email_change, name="accounts_email_change"),
    path("buy/points", accounts_buy_points, name="accounts_buy_points"),
    path("contact", accounts_contact, name="accounts_contact"),
]
