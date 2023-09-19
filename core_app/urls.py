from django.urls import path, re_path
from . import views

urlpatterns = [
    path("jobposting/", views.JobPostingLogic.as_view(), name="jobposting"),
    path("jobcategory/<int:profession_id>/", views.JobsByProfesion.as_view(), name="jobcategory"),
    path("completejob/<slug:slug>/", views.CompleteJobTask.as_view(), name="completejob"),
    re_path(r'^jobassign/(?P<user_id>\d+)/(?P<slug>.+)/$', views.JobAssignmentLogic.as_view(), name="jobassign"),
    path("freepros/<int:profession_id>/", views.FreeProsLogic.as_view(), name="freepros"),
]