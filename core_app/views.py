from rest_framework.decorators import APIView 
from rest_framework.request import Request
from .models import  JobPosting, Userprofile, JobAssignment
from rest_framework import status
from .serializers import  JobPostingSerializer, JobAssignmentSerializer
from core_auth.serializers import UserProfileSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.

class JobPostingLogic(APIView):
    # Home page to display available jobs of the same profession tag with the request.user
    def get(self, request:Request):
        job_posting = JobPosting.objects.filter(
            profession=request.user.user_profile.profession,
            status = "NA"
        )
        serializer = JobPostingSerializer(instance=job_posting, many=True)
        response = {
            "message": "These are the lists of Non allocated jobs of the same profession with the user",
            "data":serializer.data
        }

        return Response(data=response, status=status.HTTP_200_OK)

    # This sets newly posted jobs by the consumer to "Not Allocated"
    def post(self, request:Request):
        data = request.data
        serializer = JobPostingSerializer( data=data)

        if serializer.is_valid():
            
            serializer.save(poster=self.request.user, status="NA")

            response = {
                "message":"Job posting created!!!",
                "data":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Assign Jobs to professionals by the consumer and change the status of those jobs to "Pending"
class JobAssignmentLogic(APIView):
    def get(self,request:Request, user_id, slug):
        userr = User.objects.get(pk = user_id)
        job_posting = JobPosting.objects.get(slug = slug)
        already_assigned = JobAssignment.objects.filter(job = job_posting, assignee = userr)

        if request.user == job_posting.poster:
            if not already_assigned:
                job_post = JobPosting.objects.update_or_create(slug=slug, defaults={"status": "P"})
                for jobs in job_post:
                    job_assign = JobAssignment(job = jobs, assignee=userr)
                    job_assign.save()
                    serializer = JobAssignmentSerializer(instance = job_assign)
                    response = {
                        "message": "You have assigned this professional with this job",
                        "data": serializer.data
                    }
                    return Response(data=response, status=status.HTTP_201_CREATED)

            return Response(status=status.HTTP_400_BAD_REQUEST)


# Logic to set a job as "Completed" when finished
class CompleteJobTask(APIView):
    def get(self,request:Request, slug):
        job_post = JobPosting.objects.get(slug=slug)
        if request.user == job_post.poster:
            JobPosting.objects.update_or_create(
                slug = slug,
                defaults={"status": "C"})
            response = {
                "message": "You have set this job's status as Completed!"
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)




# Get list of "Not Allocated"(available) jobs by profession:
class JobsByProfesion(APIView):
    def get(self, request:Request, profession_id):
        job_posting = JobPosting.objects.filter(
            profession=profession_id,
            status = "NA")
        serializer = JobPostingSerializer(instance=job_posting, many=True)

        response = {
            "message": "These are all the Jobs for the profession selected",
            "data":serializer.data
        }

        return Response(data=response, status=status.HTTP_200_OK)


# Get the list of available professionals by profession(professionals whose assigned job reads "C", and one who has never had any assigned job before):
class FreeProsLogic(APIView):
    def get(self, request:Request, profession_id):
        userr = User.objects.filter(
            Q(job_assignee__job__status = "C") | Q(job_assignee__isnull = True)
        )
        user = Userprofile.objects.filter(
            user__in=userr,
            profession = profession_id)
        serializer = UserProfileSerializer(instance=user, many=True)
        response = {
            "message": "These are the available professionals for the selected profession",
            "serializer": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)