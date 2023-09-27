from django.contrib.auth.models import User
from rest_framework import serializers, validators
from core_app.models import Userprofile, Rating, Review


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
        }
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userprofile
        fields =  ['user','profession','bio','price','phone_number','email','state','gender']
        extra_kwargs = {
        "user" : {
            "read_only" : True,
        }
    }


class RateUserSerializer(serializers.ModelSerializer):
    rating = serializers.ChoiceField(choices=Rating.rating_options, required=False)
    class Meta:
        model = Rating
        fields = ['end_user','action_user','rating']
        extra_kwargs = {
        "end_user" : {
            "read_only" : True,
        },
        "action_user" : {
            "read_only" : True,
        }
    }


class ReviewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['end_user','action_user','review']
        extra_kwargs = {
        "end_user" : {
            "read_only" : True,
        },
        "action_user" : {
            "read_only" : True,
        }
    }