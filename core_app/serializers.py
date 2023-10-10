from rest_framework import serializers
from .models import  JobPosting, JobAssignment, Profession


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id','profession']
        extra_kwargs = {
            "id" : {"read_only" : True},
            "profession" : {"read_only" : True},
        }

class JobPostingSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=JobPosting.status_options, read_only=True, required=False)
    class Meta:
        model = JobPosting
        fields = ['poster','profession','job_description','slug','price','status']
        extra_kwargs = {
            "poster" : {"read_only" : True},
            "slug" : {"read_only" : True},
        }

class JobAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAssignment
        fields = ["job","assignee"]
