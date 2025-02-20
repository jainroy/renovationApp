from django.urls import path
from . import views

urlpatterns = [
    path('available_designers', views.available_designers,name="available_designers"),
    path('detailed_info_designer/<int:id>/',views.detailed_info_designer,name="detailed_info_designer"),
    path('designer_booking_form/<int:id>/',views.designer_booking_form,name="designer_booking_form"),
    path('designer_bookings', views.designer_bookings,name="designer_bookings"),
    path('designer_booking_detail/<int:id>/',views.designer_booking_detail,name="designer_booking_detail"),
    path('available_contractors', views.available_contractors,name="available_contractors"),
]