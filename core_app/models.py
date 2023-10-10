from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
import uuid


# Create your models here.
class Profession(models.Model):
    id = models.AutoField(primary_key=True)
    profession = models.CharField(max_length=264, blank=False)

    def __str__(self):
        return f"{self.profession}"



class StateLga(models.Model):
    name = models.CharField(max_length=264)
    state = models.ForeignKey("self", on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_profile')
    profession = models.ForeignKey(Profession, on_delete=models.DO_NOTHING, related_name= 'user_profession')
    profile_pic = models.ImageField(upload_to='profile_pic', null = True, blank = True)
    bio = models.CharField(max_length=264, verbose_name="Write a short bio about yourself")
    pricing_rate = MoneyField(max_digits=10, decimal_places=2, default_currency='NGN')
    phone_number = models.IntegerField()
    email = models.EmailField(max_length = 254)
    state = models.ForeignKey(StateLga, on_delete=models.DO_NOTHING, null=True, related_name= 'user_state')
    gender_options = (
        ('M','Male'),
        ('F','Female')
    )
    gender = models.CharField(blank = False, choices=gender_options , max_length = 10,)
    
    def __str__(self):
        return '{}'.format(self.user)


class Base(models.Model):
    end_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enduser_%(class)s",)
    action_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actionuser_%(class)s",)

    class Meta:
        abstract = True


class Rating(Base):
    rating_options = (
        ('1','Very Unsatisfied'),
        ('2','Unsatisfied'),
        ('3','Neutral'),
        ('4','Satisfied'),
        ('5','Very Satisfied'),
    )
    rating = models.CharField(blank = False, choices=rating_options , max_length = 100,)


class Review(Base):
    review = models.TextField()

    def __str__(self):
        return '{}'.format(self.end_user)


class JobPosting(models.Model):
    def foo():
        return 'abia'
    
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "job_poster")
    profession = models.ForeignKey(Profession,on_delete=models.CASCADE, related_name="job_profession")
    job_description = models.TextField()
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    slug = models.SlugField(max_length=264, unique=True, default=uuid.uuid1)
    location = models.ForeignKey(StateLga, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="job_location")
    status_options = (
        ('NA','Not Allocated'),
        ('P','Pending'),
        ('C','Completed')
    )
    status = models.CharField(choices=status_options , max_length = 10)



class JobAssignment(models.Model):
    job = models.OneToOneField(JobPosting,on_delete=models.CASCADE,related_name="job_assign")
    assignee = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="job_assignee") 