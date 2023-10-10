from rest_framework.decorators import APIView 
from rest_framework.request import Request
from .models import  JobPosting, Userprofile, JobAssignment, Profession
from rest_framework import status, permissions
from .serializers import  JobPostingSerializer, JobAssignmentSerializer, ProfessionSerializer
from core_auth.serializers import UserProfileSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

################
#### GET THE LIST OF ALL PROFESSIONS
#################

class AllProfessions(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Get the list of all professions", operation_description="THIS IS THE LIST OF ALL PROFESSIONS BY PROFESSIONALS IN PROASSIST", tags=['Professions'])

    def get(self, request:Request):
        professions = Profession.objects.all()
        serializer = ProfessionSerializer(instance=professions, many=True)
        response = {
            "MESSAGE": "This is the list of all professions by professionals in ProAssist",
            "PROFESSIONS": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)



############
#### JOB OPENINGS:
############

class JobPostingLogic(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    #### HOME PAGE to display available jobs of the same profession tag with the request.user
    @swagger_auto_schema(operation_summary="This serves data for the HOME PAGE", operation_description="THIS ENDPOINT SERVES DATA FOR THE HOMEPAGE OF THE PROFESSIONALS. FOR NON AUTHENTICATED USERS, ALL NON ALLOCATED JOB POSTINGS ARE DISPLAYED BUT FOR AUTHENTICATED USERS(PROFESSIONALS) NON-ALLOCATED JOB OPENINGS TAGGED WITH THE SAME PROFESSION AS THAT OF THE PROFESSIONAL ARE DISPLAYED(JOB OPENINGS ARE POSTED BY CONSUMERS IN NEED OF A SERVICE)\n\n THEY ARE VARIOUS STATUS FOR JOBS; 'NA' FOR NOT ALLOCATED(JOBS WITH NO ASSIGNED PROFESSIONAL), 'P' FOR PENDING(JOBS STILL ATTENDED TO BY A PROFESSIONAL), 'C' FOR COMPLETED(JOBS COMPLETED BY A PROFESSIONAL)", tags=['Job Posting'])

    def get(self, request:Request):
        # JOB POSTINGS DISPLAYED FOR NON AUTHENTICATED USERS
        if not self.request.user.is_authenticated:
            job_posting = JobPosting.objects.filter(
                status = "NA"
            )
            serializer = JobPostingSerializer(instance=job_posting, many=True)
            response = {
                "MESSAGE": "These are the lists of ALL 'NA'(Not-allocated) jobs for NON-Authenticated users",
                "JOB_OPENINGS":serializer.data
            }

            return Response(data=response, status=status.HTTP_200_OK)
        # JOB POSTINGS DISPLAYED FOR AUTHENTICATED USERS
        else:
            userr = Userprofile.objects.filter(user=request.user)
            if userr:
                userr = Userprofile.objects.get(user=self.request.user)
                job_posting = JobPosting.objects.filter(
                    profession=request.user.user_profile.profession,
                    status = "NA"
                )
                serializer = JobPostingSerializer(instance=job_posting, many=True)
                response = {
                    "MESSAGE": "These are the lists of Non allocated jobs of the same profession with the professional",
                    "JOB_OPENINGS":serializer.data
                }

                return Response(data=response, status=status.HTTP_200_OK)
            else:
                return Response({'Message': 'You have no UserProfile!'}, status = status.HTTP_400_BAD_REQUEST)

    #### To create jobs by consumers with such jobs automatically set as Not-Allocated
    @swagger_auto_schema(operation_summary="Create job openings for professionals", operation_description="THIS ENDPOINT ALLOWS CONSUMERS TO CREATE JOB OPENINGS WHICH ARE AUTOMATICALLY SET TO 'NA'(NOT-ALLOCATED)", request_body=JobPostingSerializer(), tags=['Job Posting'])

    def post(self, request:Request):
        data = request.data
        serializer = JobPostingSerializer( data=data)

        if serializer.is_valid():
            
            serializer.save(poster=self.request.user, status="NA")

            response = {
                "MESSAGE":"Job posting created!!!",
                "JOB_OPENING":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



########
### GET LIST OF ALL "NOT ALLOCATED"(AVAILABLE) JOBS BY PROFESSION:
#######

class JobsByProfesion(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(operation_summary="Get all Non allocated jobs by profession", operation_description="THIS ENDPOINT IS TO GET THE LIST OF ALL 'NOT-ALLOCATED' JOBS CATEGORIZED BY PROFESSION", tags=['Job Posting'])

    def get(self, request:Request, profession):
        professions = Profession.objects.get(profession=profession)
        job_posting = JobPosting.objects.filter(
            profession=professions,
            status = "NA")
        serializer = JobPostingSerializer(instance=job_posting, many=True)

        response = {
            "message": "These are all the (NOT-Allocated)Jobs for the profession selected",
            "data":serializer.data
        }

        return Response(data=response, status=status.HTTP_200_OK)


##########
##### LOGIC TO HELP CONSUMERS ASSIGN A JOB TO A PROFESSIONAL WITH JOB STATUS AUTOMATICALLY SET AS "PENDING":
#########

class JobAssignmentLogic(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Assign a job to a professional", operation_description="THIS ENDPOINT ALLOWS CONSUMERS TO ASSIGN A JOB TO A PROFESSIONAL WITH THAT JOB STATUS AUTOMATICALLY SET AS 'PENDING'", tags=['Job Posting'])

    def get(self,request:Request, pros_username, job_slug):
        pro_user = User.objects.get(username = pros_username)
        job_posting = JobPosting.objects.get(slug = job_slug)
        already_assigned = JobAssignment.objects.filter(job = job_posting, assignee = pro_user)

        if request.user == job_posting.poster:
            if not already_assigned:
                job_post = JobPosting.objects.update_or_create(slug=job_slug, defaults={"status": "P"})
                for jobs in job_post:
                    job_assign = JobAssignment(job = jobs, assignee=pro_user)
                    job_assign.save()
                    pending_job = JobPosting.objects.get(slug=job_slug)
                    serializer = JobAssignmentSerializer(instance = job_assign)
                    job_serializer = JobPostingSerializer(instance=pending_job)
                    response = {
                        "MESSAGE": "You have assigned this professional with this job",
                        "JOB_ASSIGNMENT": serializer.data,
                        "JOB_ASSIGNED": job_serializer.data
                    }
                    return Response(data=response, status=status.HTTP_201_CREATED)

            return Response(status=status.HTTP_400_BAD_REQUEST)


#########
###### LOGIC TO SET A JOB AS "COMPLETED" WHEN FINISHED BY THE CONSUMER
#########

class CompleteJobTask(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Update a job as completed", operation_description="THIS ENDPOINT ALLOWS CONSUMERS TO UPDATE A JOB AS COMPLETED AFTER A PROFESSIONAL HAS RENDERED THE REQUESTED SERVICE IN THE JOB", tags=['Job Posting'])

    def get(self,request:Request, job_slug):
        job_post = JobPosting.objects.get(slug=job_slug)
        if request.user == job_post.poster:
            JobPosting.objects.update_or_create(
                slug = job_slug,
                defaults={"status": "C"})
            jobs=JobPosting.objects.get(slug=job_slug)
            serializer = JobPostingSerializer(instance=jobs)
            response = {
                "MESSAGE": "You have set this job's status as Completed!",
                'COMPLETED_JOB': serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



###########
## GET THE LIST OF AVAILABLE PROFESSIONALS BY PROFESSION(PROFESSIONALS WHOSE ASSIGNED JOB READS "C", AND ONE WHO HAS NEVER HAD ANY ASSIGNED JOB BEFORE):
############

class FreeProsLogic(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(operation_summary="Get free professionals by profession", operation_description="THIS ENDPOINT ALLOWS CONSUMERS TO GET AVAILABLE PROFESSIONALS BY PROFESSION i.e PROFESSIONALS WITH NO JOBS PENDING", tags=['Free Professionals'])

    def get(self, request:Request, profession):
        professions = Profession.objects.get(profession=profession)
        userr = User.objects.filter(
            Q(job_assignee__job__status = "C") | Q(job_assignee__isnull = True)
        )
        user = Userprofile.objects.filter(
            user__in=userr,
            profession = professions)
        serializer = UserProfileSerializer(instance=user, many=True)
        response = {
            "MESSAGE": "These are the available professionals for the selected profession",
            "FREE_PROS": serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)