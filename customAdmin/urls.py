from django.urls import path, include
import django.contrib.admin as admin

from .views import *
import customAdmin.sub_views.site as site
import customAdmin.sub_views.prefecture as prefectures
import customAdmin.sub_views.category as categories
import customAdmin.sub_views.skill as skills
import customAdmin.sub_views.workhour as workhours
import customAdmin.sub_views.worktype as worktypes
import customAdmin.sub_views.employee as employees
import customAdmin.sub_views.employer as employers
import customAdmin.sub_views.job as jobs
import customAdmin.sub_views.message as messages

urlpatterns = [
    path("login", admin_login, name="admin_login"),
    path("password/change", admin_password_change, name = "admin_password_change"),
    path("jobs", jobs.index, name="admin_jobs"),
    path("jobs/new", jobs.new, name="admin_jobs_new"),
    path("jobs/info", jobs.info, name="admin_jobs_info"),
    path("jobs/delete", jobs.delete, name="admin_jobs_delete"),
    path("jobs/active", jobs.job_active, name="admin_jobs_active"),
    path("jobs/active_all", jobs.job_active_all, name="admin_jobs_active_all"),
    path("employees", employees.index, name="admin_employees"),
    path("employees/update", employees.update, name="admin_employees_update"),
    path("employees/delete", employees.delete, name="admin_employees_delete"),
    path("employers", employers.index, name="admin_employers"),
    path("employers/update", employers.update, name="admin_employers_update"),
    path("employers/delete", employers.delete, name="admin_employers_delete"),
    path("messages", messages.index, name="admin_messages"),
    path("messages/<id>", messages.info, name="admin_message_info"),
    path("sites", site.index, name="admin_sites"),
    path("sites/update", site.update, name="admin_sites_update"),
    path("prefectures", prefectures.index, name="admin_prefectures"),
    path("prefectures/create", prefectures.create, name="admin_prefectures_create"),
    path("prefectures/update", prefectures.update, name="admin_prefectures_update"),
    path("prefectures/delete", prefectures.delete, name="admin_prefectures_delete"),
    path("categories", categories.index, name="admin_categories"),
    path("categories/create", categories.create, name="admin_categories_create"),
    path("categories/update", categories.update, name="admin_categories_update"),
    path("categories/delete", categories.delete, name="admin_categories_delete"),
    path("skills", skills.index, name="admin_skills"),
    path("skills/create", skills.create, name="admin_skills_create"),
    path("skills/update", skills.update, name="admin_skills_update"),
    path("skills/delete", skills.delete, name="admin_skills_delete"),
    path("workhours", workhours.index, name="admin_workhours"),
    path("workhours/create", workhours.create, name="admin_workhours_create"),
    path("workhours/update", workhours.update, name="admin_workhours_update"),
    path("workhours/delete", workhours.delete, name="admin_workhours_delete"),
    path("worktypes", worktypes.index, name="admin_worktypes"),
    path("worktypes/create", worktypes.create, name="admin_worktypes_create"),
    path("worktypes/update", worktypes.update, name="admin_worktypes_update"),
    path("worktypes/delete", worktypes.delete, name="admin_worktypes_delete"),
    path("email/change", email_change, name="admin_email_change"),
    path("", index, name="admin_index"),
]
