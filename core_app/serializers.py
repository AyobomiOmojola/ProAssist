from rest_framework import serializers
from .models import  JobPosting, JobAssignment




class JobPostingSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=JobPosting.status_options, required=False)
    class Meta:
        model = JobPosting
        fields = ['poster','profession','job_description','price','location','status']
        extra_kwargs = {
            "poster" : {"read_only" : True},
            "status" : {"read_only" : True},
        }

class JobAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAssignment
        fields = ["job","assignee"]
