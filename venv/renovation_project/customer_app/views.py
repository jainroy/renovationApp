from django.conf import settings
from django.shortcuts import redirect, render
from renovation_app.models import * # type: ignore
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DesignerRoomFormSet, ContractorRoomFormSet, FeedbackForm
from django.shortcuts import get_object_or_404, redirect, render
from .models import Booking, RoomDetails, DesignPreference
from django.core.mail import send_mail



# Create your views here.
def available_designers(request):
    designers = Register.objects.filter(usertype='designer', is_approved=True)
    return render(request, 'available_designers.html', {'designers': designers})

def detailed_info_designer(request, id):
    designer = Register.objects.get(id=id)
    return render (request, 'detailed_info_designer.html', {'designer': designer})

def designer_booking_form(request, id):
    designer = get_object_or_404(Register, id=id)

    if request.method == 'POST':
        formset = DesignerRoomFormSet(request.POST, prefix='rooms')  # ✅ Add prefix

        print("Form data received:", formset.data)  # Debugging

        if formset.is_valid():
            user = request.user  # ✅ Fix user instance
            print("User:", user)

            # ✅ Create booking
            booking = Booking.objects.create(
                user=user,
                designer=designer,
                status='pending'
            )
            print("Booking Created:", booking)

            # ✅ Process formset
            for form in formset:
                if form.is_valid():  # ✅ Check form validity
                    cleaned_data = form.cleaned_data

                    # ✅ Create DesignPreference
                    design_preference = DesignPreference.objects.create(
                        design_type=cleaned_data['design_type'],
                        floor_type=cleaned_data['floor_type'],
                        wall_paint_color=cleaned_data['wall_paint_color'],
                        ceiling_type=cleaned_data['ceiling_type'],
                        lighting_preference=cleaned_data['lighting_preference'],
                        budget_range=cleaned_data['budget_range'],
                        description=cleaned_data['description'],
                    )
                    print("Design Preference Created:", design_preference)
                    # ✅ Create RoomDetails
                    room_details = RoomDetails.objects.create(
                        room_type=cleaned_data['room_type'],
                        room_area=cleaned_data['room_area'],
                        design_preference=design_preference,  # ✅ Fix field name
                        booking=booking
                    )
                    print("Room Details Created:", room_details)
            subject="New Service Request Notification"
            message=f"Dear {designer.username}, you have received a new service request. Please check your account for details and respond promptly. Thank you!"
            email_from=settings.EMAIL_HOST_USER
            email_to=[designer.email]
            send_mail(subject, message, email_from, email_to)
            messages.success(request, "Booking request has been sent.", extra_tags='success')
            return redirect('designer_bookings')
        else:
            print("Formset errors:", formset.errors)  # ✅ Debugging
    else:
        formset = DesignerRoomFormSet(prefix='rooms')  # ✅ Prefix
    return render(request, 'designer_booking_form.html', {'formset': formset})

def designer_bookings(request):
    id = request.user.id
    bookings = Booking.objects.filter(
        user=id,  # Ensures the logged-in user is the requester
        rooms__design_preference__isnull=False  # Ensures only contractor-related bookings
    ).distinct().prefetch_related('rooms__design_preference')

    return render(request, 'designer_bookings.html', {'bookings': bookings})

def designer_booking_detail(request, id):
    booking = Booking.objects.select_related('user', 'designer').prefetch_related(
        'rooms__design_preference'
    ).get(id=id)
    
    return render(request, 'designer_booking_detail.html', {'booking': booking})

def cancel_designer_booking(request, id):
    booking = Booking.objects.get(id=id)
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
def contractor_booking_form(request, id):
    contractor = get_object_or_404(Register, id=id)

    if request.method == 'POST':
        formset = ContractorRoomFormSet(request.POST, prefix='rooms')  # ✅ Add prefix

        print("Form data received:", formset.data)  # Debugging

        if formset.is_valid():
            user = request.user  # ✅ Fix user instance
            print("User:", user)

            # ✅ Create booking
            booking = Booking.objects.create(
                user=user,
                contractor=contractor,
                status='pending'
            )
            print("Booking Created:", booking)

            # ✅ Process formset
            for form in formset:
                if form.is_valid():  # ✅ Check form validity
                    cleaned_data = form.cleaned_data

                    # ✅ Create DesignPreference
                    contract_preference = ContractPreference.objects.create(
                        project_type=cleaned_data['project_type'],
                        floor_type=cleaned_data['floor_type'],
                        wall_finish=cleaned_data['wall_finish'],
                        ceiling_type=cleaned_data['ceiling_type'],
                        lighting_preference=cleaned_data['lighting_preference'],
                        budget_range=cleaned_data['budget_range'],
                        description=cleaned_data['description'],
                    )
                    print("Contract Preference Created:", contract_preference)

                    # ✅ Create RoomDetails
                    room_details = RoomDetails.objects.create(
                        room_type=cleaned_data['room_type'],
                        room_area=cleaned_data['room_area'],
                        contract_preference=contract_preference,  # ✅ Fix field name
                        booking=booking
                    )
                    print("Room Details Created:", room_details)
            subject="New Service Request Notification"
            message=f"Dear {contractor.username}, you have received a new service request. Please check your account for details and respond promptly. Thank you!"
            email_from=settings.EMAIL_HOST_USER
            email_to=[contractor.email]
            send_mail(subject, message, email_from, email_to)
            messages.success(request, "Booking request has been sent.", extra_tags='success')
            return redirect('contractor_bookings')

        else:
            print("Formset errors:", formset.errors)  # ✅ Debugging

    else:
        formset = ContractorRoomFormSet(prefix='rooms')  # ✅ Prefix

    return render(request, 'contractor_booking_form.html', {'formset': formset})


def contractor_bookings(request):
    id = request.user.id
    bookings = Booking.objects.filter(
        user=id,  # Ensures the logged-in user is the requester
        rooms__contract_preference__isnull=False  # Ensures only contractor-related bookings
    ).distinct().prefetch_related('rooms__contract_preference')

    return render(request, 'contractor_bookings.html', {'bookings': bookings})


def contractor_booking_detail(request, id):
    booking = Booking.objects.select_related('user', 'contractor').prefetch_related(
        'rooms__contract_preference'
    ).get(id=id)
    
    return render(request, 'contractor_booking_detail.html', {'booking': booking})


def cancel_contractor_booking(request, id):
    booking = Booking.objects.get(id=id)
    booking.status = "canceled"  # Updating status
    booking.save()
    messages.success(request, "Booking has been canceled.")
    return redirect('contractor_booking_detail', id=id)

def add_feedback(request,id):
    booking= Booking.objects.get(id=id)
    designer = booking.designer
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.designer = designer
            feedback.booking = booking
            feedback.user = request.user  # Assign logged-in user to feedback
            feedback.save()
            return redirect('designer_booking_detail', feedback.booking.id)  # Redirect after submission
    else:
        form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})
def add_contractor_feedback(request,id):
    booking= Booking.objects.get(id=id)
    contractor = booking.contractor
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.contractor = contractor
            feedback.booking = booking
            feedback.user = request.user  # Assign logged-in user to feedback
            feedback.save()
            return redirect('contractor_booking_detail', feedback.booking.id)  # Redirect after submission
    else:
        form = FeedbackForm()
    return render(request, 'feedback_form.html', {'form': form})

def view_feedback(request,id):
    booking = Booking.objects.get(id=id)
    feedbacks = Feedback.objects.filter(booking=booking).order_by('-created_at')  # Retrieve all feedbacks
    return render(request, 'view_feedback.html', {'feedbacks': feedbacks})