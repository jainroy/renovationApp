from django.urls import path
from . import views

urlpatterns = [
    path('designer_service_requests', views.designer_service_requests,name="designer_service_requests"),
    path('designer_service_request_detail/<int:id>/',views.designer_service_request_detail,name="designer_service_request_detail"),
    path('approve_designer_request/<int:id>/', views.approve_designer_request, name="approve_designer_request"),
    path('reject_designer_request/<int:id>/', views.reject_designer_request, name="reject_designer_request"),
    
]