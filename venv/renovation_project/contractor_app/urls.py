from django.urls import path
from . import views

urlpatterns = [
    path('contractor_service_requests', views.contractor_service_requests,name="contractor_service_requests"),
    path('contractor_service_request_detail/<int:id>/',views.contractor_service_request_detail,name="contractor_service_request_detail"),
    path('approve_contractor_request/<int:id>/', views.approve_contractor_request, name="approve_contractor_request"),
    path('reject_contractor_request/<int:id>/', views.reject_contractor_request, name="reject_contractor_request"),
    
]