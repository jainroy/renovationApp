from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user_login/', views.user_login,name="user_login"),
    path('registration', views.registration, name="registration"),
    path('home', views.home, name = "home"),
    path('user_logout/', views.user_logout, name = "user_logout"),
    path('single/', views.single, name = "single"),
    path('view_user', views.view_user, name = "view_user"),
    path('profile', views.profile, name = "profile"),
    path('update_profile', views.update_profile, name = "update_profile"),
    path('forgot_password', views.forgot_password, name = "forgot_password"),
    path('reset_password', views.reset_password, name = "reset_password"),
    path('delete_user/<int:id>/', views.delete_user, name = "delete_user"),
    path('registration_type', views.registration_type, name = "registration_type"),
    path('designer_registration', views.designer_registration, name="designer_registration"),
    path('designer_profile', views.designer_profile, name = "designer_profile"),
]