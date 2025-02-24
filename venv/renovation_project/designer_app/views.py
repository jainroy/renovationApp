from django.shortcuts import redirect, render
from renovation_app.models import * # type: ignore
from customer_app.models import DesignerBooking # type: ignore
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *

def designer_service_requests(request):
    id = request.user.id
    requests = DesignerBooking.objects.filter(designer=id).exclude(status__in=['canceled', 'rejected'])
    return render (request, 'designer_service_requests.html', {'requests': requests})
def designer_service_request_detail(request, id):
    booking = DesignerBooking.objects.get(id=id)  # Use a different variable name
    return render(request, 'designer_service_request_detail.html', {'booking': booking})
def approve_designer_request(request, id):
    booking = DesignerBooking.objects.get(id=id)
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, "Booking request has been approved.")
    return redirect('designer_service_requests')

def reject_designer_request(request, id):
    booking = DesignerBooking.objects.get(id=id)
    booking.status = 'rejected'
    booking.save()
    messages.error(request, "Booking request has been rejected.")
    return redirect('designer_service_requests')