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


class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            user = serializer.save()


            response = {
                "message": "User Created Successfully", 
                "data": serializer.data,
                #'token' : token.key
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request: Request):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username = username, password = password)
            token, created = Token.objects.get_or_create(user=user)

            response = {
                "message": "Login Successfull", 
                "tokens": token.key
            }

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password",})

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)



class LogoutView(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)


class RateUser(APIView):
    def post(self, request:Request, user_id):
        enduser = User.objects.get(pk = user_id)
        actionuser = request.user
        data = request.data
        serializer = RateUserSerializer(data = data)

        if serializer.is_valid():
            serializer.save(end_user=enduser,action_user=actionuser)

            response = {
                "message":"You rated this user!",
                "data":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewUser(APIView):
    def post(self, request:Request, user_id):
        enduser = User.objects.get(pk = user_id)
        actionuser = request.user
        data = request.data
        serializer = ReviewUserSerializer(data = data)

        if serializer.is_valid():
            serializer.save(end_user=enduser,action_user=actionuser)

            response = {
                "message":"You reviewed this user!",
                "data":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateUserProfile(APIView):
    def post(self, request:Request):
        data = request.data

        serializer = UserProfileSerializer(data=data)

        if serializer.is_valid():

            serializer.save(user=self.request.user)

            response = {
                "message":"UserProfile Created",
                "data":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request:Request):
        userprofile = Userprofile.objects.get(user = request.user)
        user_serializer = UserProfileSerializer(instance=userprofile)

        # To get rating of user
        ratings = Rating.objects.filter(end_user = request.user)
        rate_serializer = RateUserSerializer(instance=ratings, many=True)

        # In order to get reviews of user:
        reviews = Review.objects.filter(end_user = request.user)
        review_serializer = ReviewUserSerializer(instance=reviews, many=True)

        # To get Pending jobs of users:
        pending_jobs = JobPosting.objects.filter(
            job_assign__assignee = request.user,
            status = 'P'
        )
        pending_jobs_serializer = JobPostingSerializer(instance = pending_jobs, many = True)

        # To get Completed jobs of user:
        completed_jobs = JobPosting.objects.filter(
            job_assign__assignee = request.user,
            status = 'C'
        )
        completed_jobs_serializer = JobPostingSerializer(instance = completed_jobs, many = True)

        response = {
                "message":"UserProfile of logged-in user",
                "UserProfile_data":user_serializer.data,
                "rate_serializer":rate_serializer.data,
                "review_serializer":review_serializer.data,
                "pending_jobs_serializer":pending_jobs_serializer.data,
                "completed_jobs_serializer":completed_jobs_serializer.data
            }

        return Response(data=response, status=status.HTTP_200_OK)
    
    def put(self, request:Request):
        userprofile = Userprofile.objects.get(user = request.user)
        data = request.data
        serializer = UserProfileSerializer(instance=userprofile, data=data)

        if serializer.is_valid():

            serializer.save(user=self.request.user)

            response = {
                "message":"UserProfile Updated!!!",
                "data":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)


class OtherUserProfile(APIView):
    def get(self, request:Request, user_id):
        userprofile = Userprofile.objects.get(user = user_id)
        user_serializer = UserProfileSerializer(instance=userprofile)

        # To get rating of user
        ratings = Rating.objects.filter(end_user = user_id)
        rate_serializer = RateUserSerializer(instance=ratings, many=True)

        # In order to get reviews of  user:
        reviews = Review.objects.filter(end_user = user_id)
        review_serializer = ReviewUserSerializer(instance=reviews, many=True)

        # To get Pending jobs of users:
        pending_jobs = JobPosting.objects.filter(
            job_assign__assignee = user_id,
            status = 'P'
        )
        pending_jobs_serializer = JobPostingSerializer(instance = pending_jobs, many = True)

        # To get Completed jobs of user:
        completed_jobs = JobPosting.objects.filter(
            job_assign__assignee = user_id,
            status = 'C'
        )
        completed_jobs_serializer = JobPostingSerializer(instance = completed_jobs, many = True)

        response = {
                "message":"UserProfile of other user",
                "UserProfile_data":user_serializer.data,
                "rate_serializer":rate_serializer.data,
                "review_serializer":review_serializer.data,
                "pending_jobs_serializer":pending_jobs_serializer.data,
                "completed_jobs_serializer":completed_jobs_serializer.data
            }

        return Response(data=response, status=status.HTTP_200_OK)