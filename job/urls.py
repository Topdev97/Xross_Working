from django.urls import path

import job.views as job

urlpatterns = [
    path("search", job.index, name="job_index"),
    path("workspace", job.workspace, name="job_workspace"),
    path("favourites", job.favourites, name="job_favourites"),
    path("<id>", job.info, name="job_info"),
    path("<id>/like", job.like, name="job_like"),
    path("<id>/favourite", job.favourite, name="job_favourite"),
]
