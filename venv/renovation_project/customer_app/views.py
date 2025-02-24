from django.shortcuts import redirect, render
from renovation_app.models import * # type: ignore
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *



# Create your views here.
def available_designers(request):
    designers = Register.objects.filter(usertype='designer', is_approved=True)
    return render(request, 'available_designers.html', {'designers': designers})

def designer_bookings(request):
    id = request.user.id
    bookings = DesignerBooking.objects.filter(user=id).exclude(status__in=['rejected'])
    return render (request, 'designer_bookings.html', {'bookings': bookings})

def detailed_info_designer(request, id):
    designer = Register.objects.get(id=id)
    return render (request, 'detailed_info_designer.html', {'designer': designer})


# View to create a booking for the selected designer
@login_required
def designer_booking_form(request, id):
    # Fetch the designer from the Register model
    designer = Register.objects.get(id=id)
    
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (POST)
        form = DesignerBookingForm(request.POST)
        if form.is_valid():
            # Create the booking instance but do not save it yet
            booking = form.save(commit=False)
            booking.user = request.user  # Set the logged-in user
            booking.designer = designer  # Set the selected designer
            booking.save()  # Save the booking instance
            messages.success(request, "Booking created successfully.", extra_tags="success")
            return redirect('designer_bookings')  # Redirect to a success page (or booking confirmation)
    else:
        form = DesignerBookingForm()  # Instantiate the form if it's a GET request

    # Render the booking form template and pass the form and designer to the template
    return render(request, 'designer_booking_form.html', {'form': form, 'designer': designer, 'title':'Update'})

def designer_booking_detail(request, id):
    booking = DesignerBooking.objects.get(id=id)
    return render (request, 'designer_booking_detail.html', {'booking': booking})

def cancel_designer_booking(request, id):
    booking = DesignerBooking.objects.get(id=id)
    booking.status = "canceled"  # Updating status
    booking.save()
    messages.success(request, "Booking has been canceled.")
    return redirect('designer_booking_detail', id=id)

def available_contractors(request):
    contractors = Register.objects.filter(usertype='contractor', is_approved=True)
    return render(request, 'available_contractors.html', {'contractors': contractors})

def detailed_info_contractor(request, id):
    contractor = Register.objects.get(id=id)
    return render (request, 'detailed_info_contractor.html', {'contractor': contractor})
# View to create a booking for the selected contractor
@login_required
def contractor_booking_form(request, id):
    # Fetch the contractor from the Register model
    contractor = Register.objects.get(id=id)
    
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (POST)
        form = ContractorBookingForm(request.POST)
        if form.is_valid():
            # Create the booking instance but do not save it yet
            booking = form.save(commit=False)
            booking.user = request.user  # Set the logged-in user
            booking.contractor = contractor  # Set the selected contractor
            booking.save()  # Save the booking instance
            messages.success(request, "Booking created successfully.", extra_tags="success")
            return redirect('contractor_bookings')  # Redirect to a success page (or booking confirmation)
    else:
        form = ContractorBookingForm()  # Instantiate the form if it's a GET request

    # Render the booking form template and pass the form and contractor to the template
    return render(request, 'contractor_booking_form.html', {'form': form, 'contractor': contractor, 'title': 'Update'})
def contractor_bookings(request):
    id = request.user.id
    bookings = ContractorBooking.objects.filter(user=id).exclude(status__in=['rejected'])
    return render (request, 'contractor_bookings.html', {'bookings': bookings})

def contractor_booking_detail(request, id):
    booking = ContractorBooking.objects.get(id=id)
    return render (request, 'contractor_booking_detail.html', {'booking': booking})
def cancel_contractor_booking(request, id):
    booking = ContractorBooking.objects.get(id=id)
    booking.status = "canceled"  # Updating status
    booking.save()
    messages.success(request, "Booking has been canceled.")
    return redirect('contractor_booking_detail', id=id)
