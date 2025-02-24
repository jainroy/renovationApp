from django.urls import path
from . import views

urlpatterns = [
    path('available_designers', views.available_designers,name="available_designers"),
    path('detailed_info_designer/<int:id>/',views.detailed_info_designer,name="detailed_info_designer"),
    path('designer_booking_form/<int:id>/',views.designer_booking_form,name="designer_booking_form"),
    path('designer_bookings', views.designer_bookings,name="designer_bookings"),
    path('designer_booking_detail/<int:id>/',views.designer_booking_detail,name="designer_booking_detail"),
    path('cancel_designer_booking/<int:id>/',views.cancel_designer_booking,name="cancel_designer_booking"),
    path('available_contractors', views.available_contractors,name="available_contractors"),
    path('detailed_info_contractor/<int:id>/',views.detailed_info_contractor,name="detailed_info_contractor"),
    path('contractor_booking_form/<int:id>/',views.contractor_booking_form,name="contractor_booking_form"),
    path('contractor_bookings', views.contractor_bookings,name="contractor_bookings"),
    path('contractor_booking_detail/<int:id>/',views.contractor_booking_detail,name="contractor_booking_detail"),
    path('cancel_contractor_booking/<int:id>/',views.cancel_contractor_booking,name="cancel_contractor_booking"),
]