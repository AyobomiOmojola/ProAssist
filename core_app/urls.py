from django.urls import path, re_path
from . import views

urlpatterns = [
    path("allprofessions/", views.AllProfessions.as_view(), name="allprofessions"),
    path("jobposting/", views.JobPostingLogic.as_view(), name="jobposting"),
    path("jobcategory/<profession>/", views.JobsByProfesion.as_view(), name="jobcategory"),
    path("completejob/<slug:job_slug>/", views.CompleteJobTask.as_view(), name="completejob"),
    re_path(r'^jobassign/(?P<pros_username>\w+)/(?P<job_slug>.+)/$', views.JobAssignmentLogic.as_view(), name="jobassign"),
    path("freepros/<profession>/", views.FreeProsLogic.as_view(), name="freepros"),
]