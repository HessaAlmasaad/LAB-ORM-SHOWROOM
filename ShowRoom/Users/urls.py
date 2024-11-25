from django.urls import path
from . import views

app_name = "Users"

urlpatterns = [
    path('signup/', views.sign_up, name="sign_up"),
    path('signin/', views.sign_in, name="sign_in"),
    path('logout/', views.log_out, name="log_out"),
    path('profile/<user_name>/', views.user_profile_view, name="user_profile_view"),
    path('profile/update/', views.update_user_profile, name="update_user_profile"),
]