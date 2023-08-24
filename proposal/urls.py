from django.urls import path

import proposal.views as proposal


urlpatterns = [
    path("new/<id>", proposal.new, name="proposal_new"),
    path("status", proposal.proposal_status, name="set_proposal_status"),
]
