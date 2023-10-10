from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView 
from django.contrib.auth import authenticate
from rest_framework import status, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import UserProfileSerializer, RateUserSerializer, ReviewUserSerializer
from core_app.models import Userprofile, Rating, Review, JobPosting
from core_app.serializers import JobPostingSerializer
from django.contrib.sessions.middleware import SessionMiddleware
from drf_yasg.utils import swagger_auto_schema



###########
### REGISTER USERS
###########

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Register Users", request_body=RegisterSerializer, tags=['Authentication'])

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()


            response = {
                "MESSAGE": "User Created Successfully", 
                "REGISTERED_USER": serializer.data,
                #'token' : token.key
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)




###########
### LOGIN USERS
###########

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Login Users", request_body=AuthTokenSerializer, tags=['Authentication'])
    def post(self, request: Request):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username = username, password = password)
            token, created = Token.objects.get_or_create(user=user)

            response = {
                "MESSAGE": "Login Successfull", 
                "TOKEN": token.key
            }

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password",})

    @swagger_auto_schema(operation_summary="Check for authentication", tags=['Authentication'])
    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)


###########
### LOGOUT USERS
###########

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Logout Users", tags=['Authentication'])
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"MESSAGE": "You are logged out"}, status=status.HTTP_200_OK)


##########
### RATE PROFESSIONALS
##########

class RateUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(operation_summary="Rate professionals", operation_description="THIS ENDPOINT ALLOWS CONSUMERS TO RATE PROFESSIONALS FOR SERVICES RENDERED", request_body=RateUserSerializer, tags=['Rate/Review Professionals'])

    def post(self, request:Request, username):
        enduser = User.objects.get(username = username)
        actionuser = request.user
        data = request.data
        serializer = RateUserSerializer(data = data)

        if serializer.is_valid():
            serializer.save(end_user=enduser,action_user=actionuser)

            response = {
                "MESSAGE":"You rated this user!",
                "RATING": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##########
### REVIEW PROFESSIONALS
##########

class ReviewUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(operation_summary="Review professionals", operation_description="THIS ENDPOINT ALLOWS CONSUMERS WRITE A REVIEW ON PROFESSIONALS FOR SERVICES RENDERED", request_body=ReviewUserSerializer, tags=['Rate/Review Professionals'])

    def post(self, request:Request, username):
        enduser = User.objects.get(username = username)
        actionuser = request.user
        data = request.data
        serializer = ReviewUserSerializer(data = data)

        if serializer.is_valid():
            serializer.save(end_user=enduser,action_user=actionuser)

            response = {
                "MESSAGE":"You reviewed this user!",
                "REVIEW":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



##########
### USERPROFILE
##########

class CreateUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(operation_summary="Create UserProfile", request_body=UserProfileSerializer, tags=['Userprofile'])

    #### CREATE YOUR USERPROFILE
    def post(self, request:Request):
        data = request.data

        serializer = UserProfileSerializer(data=data)

        if serializer.is_valid():

            serializer.save(user=self.request.user)

            response = {
                "MESSAGE":"UserProfile Created",
                "USERPROFILE":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(operation_summary="Retrieve your userprofile", operation_description="THIS ENPOINT RETRIEVES YOUR USERPROFILE WITH YOUR RATINGS, REVIEWS PENDING AND COMPLETED JOBS(IF YOUR ARE A PROFESSIONAL)", tags=['Userprofile'])

    #### RETRIEVE YOUR USERPROFILE
    def get(self, request:Request):
        userprofile = Userprofile.objects.get(user = request.user)
        user_serializer = UserProfileSerializer(instance=userprofile)

        ### To get rating of user
        ratings = Rating.objects.filter(end_user = request.user)
        rate_serializer = RateUserSerializer(instance=ratings, many=True)

        ### In order to get reviews of user:
        reviews = Review.objects.filter(end_user = request.user)
        review_serializer = ReviewUserSerializer(instance=reviews, many=True)

        ### To get Pending jobs of users:
        pending_jobs = JobPosting.objects.filter(
            job_assign__assignee = request.user,
            status = 'P'
        )
        pending_jobs_serializer = JobPostingSerializer(instance = pending_jobs, many = True)

        ### To get Completed jobs of user:
        completed_jobs = JobPosting.objects.filter(
            job_assign__assignee = request.user,
            status = 'C'
        )
        completed_jobs_serializer = JobPostingSerializer(instance = completed_jobs, many = True)

        response = {
                "MESSAGE":"UserProfile of logged-in user",
                "USERPROFILE":user_serializer.data,
                "RATINGS":rate_serializer.data,
                "REVIEWS":review_serializer.data,
                "PENDING_JOBS":pending_jobs_serializer.data,
                "COMPLETED_JOBS":completed_jobs_serializer.data
            }

        return Response(data=response, status=status.HTTP_200_OK)
    

    ####### UPDATE YOUR USERPROFILE
    @swagger_auto_schema(operation_summary="Update Userprofile", request_body=UserProfileSerializer, tags=['Userprofile'])

    def put(self, request:Request):
        userprofile = Userprofile.objects.get(user = request.user)
        data = request.data
        serializer = UserProfileSerializer(instance=userprofile, data=data)

        if serializer.is_valid():

            serializer.save(user=self.request.user)

            response = {
                "MESSAGE":"UserProfile Updated!!!",
                "USERPROFILE":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)



#############
#### VIEW OTHER USERPROFILES
#############

class OtherUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="View other Userprofiles", operation_description="THIS ENDPOINT RETRIEVES OTHER USERPROFILES WITH THEIR RATINGS, REVIEWS, PENDING AND COMPLETED JOBS(IF YOUR ARE A PROFESSIONAL)", tags=['Userprofile'])

    def get(self, request:Request, username):
        other_user = User.objects.get(username=username)
        userprofile = Userprofile.objects.filter(user = other_user)
        if userprofile:
            user_serializer = UserProfileSerializer(instance=userprofile, many=True)

            ### To get rating of user
            ratings = Rating.objects.filter(end_user = other_user)
            rate_serializer = RateUserSerializer(instance=ratings, many=True)

            ### In order to get reviews of  user:
            reviews = Review.objects.filter(end_user = other_user)
            review_serializer = ReviewUserSerializer(instance=reviews, many=True)

            ### To get Pending jobs of users:
            pending_jobs = JobPosting.objects.filter(
                job_assign__assignee = other_user,
                status = 'P'
            )
            pending_jobs_serializer = JobPostingSerializer(instance = pending_jobs, many = True)

            ### To get Completed jobs of user:
            completed_jobs = JobPosting.objects.filter(
                job_assign__assignee = other_user,
                status = 'C'
            )
            completed_jobs_serializer = JobPostingSerializer(instance = completed_jobs, many = True)

            response = {
                    "MESSAGE":"UserProfile of other user",
                    "USERPROFILE":user_serializer.data,
                    "RATINGS":rate_serializer.data,
                    "REVIEWS":review_serializer.data,
                    "PENDNG_JOBS":pending_jobs_serializer.data,
                    "COMPLETED_JOBS":completed_jobs_serializer.data
                }

            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response({'Message': 'User has no Userprofile!'}, status = status.HTTP_400_BAD_REQUEST)
