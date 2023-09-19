from django.urls import path, re_path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.CreateUserProfile.as_view(), name="profile"),
    path("otherprofile/<int:user_id>/", views.OtherUserProfile.as_view(), name="other_profile"),
    path("rateuser/<int:user_id>/", views.RateUser.as_view(), name="rateuser"),
    path("reviewuser/<int:user_id>/", views.ReviewUser.as_view(), name="reviewuser")
]