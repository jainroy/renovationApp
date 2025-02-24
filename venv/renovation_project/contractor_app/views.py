from django.shortcuts import redirect, render
from renovation_app.models import * # type: ignore
from customer_app.models import ContractorBooking # type: ignore
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .forms import *

def contractor_service_requests(request):
    id = request.user.id
    requests = ContractorBooking.objects.filter(contractor=id).exclude(status__in=['canceled', 'rejected'])
    return render (request, 'contractor_service_requests.html', {'requests': requests})
def contractor_service_request_detail(request, id):
    booking = ContractorBooking.objects.get(id=id)  # Use a different variable name
    return render(request, 'contractor_service_request_detail.html', {'booking': booking})
def approve_contractor_request(request, id):
    booking = ContractorBooking.objects.get(id=id)
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, "Booking request has been approved.")
    return redirect('contractor_service_requests')

def reject_contractor_request(request, id):
    booking = ContractorBooking.objects.get(id=id)
    booking.status = 'rejected'
    booking.save()
    messages.error(request, "Booking request has been rejected.")
    return redirect('contractor_service_requests')