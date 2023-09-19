from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Userprofile)
admin.site.register(Review)

class JobAssignmentAdmin(admin.ModelAdmin):
    model = JobAssignment
    #inline = [JobPosting]
    list_display = ["job","assignee"]

admin.site.register(JobAssignment, JobAssignmentAdmin)

class RatingAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ["action_user","end_user","rating"]

admin.site.register(Rating, RatingAdmin)

class ProfessionAdmin(admin.ModelAdmin):
    model = Profession
    ordering = ('pk',)

admin.site.register(Profession, ProfessionAdmin)

class JobPostingAdmin(admin.ModelAdmin):
    model = JobPosting
    ordering = ('pk',)
    list_display = ["profession","status","job_description"]

admin.site.register(JobPosting, JobPostingAdmin)


class StateLgaAdmin(admin.ModelAdmin):
    model = StateLga
    ordering = ('pk',)

admin.site.register(StateLga, StateLgaAdmin)
