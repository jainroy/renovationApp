from django.conf import settings
from django.shortcuts import redirect, render
from renovation_app.models import * # type: ignore
from customer_app.models import Booking # type: ignore
from .models import *
from django.contrib import messages
from .forms import *
from django.core.mail import send_mail


def designer_service_requests(request):
    id = request.user.id
    requests = Booking.objects.filter(designer=id).exclude(status__in=['canceled', 'rejected']).prefetch_related(
        'rooms__design_preference'
    )
    return render(request, 'designer_service_requests.html', {'requests': requests})

def designer_service_request_detail(request, id):
    # Fetch the booking object with related rooms and design preferences
    booking = Booking.objects.prefetch_related(
        'rooms__design_preference'  # Prefetch related design preferences for rooms
    ).get(id=id)

    return render(request, 'designer_service_request_detail.html', {'booking': booking})
def approve_designer_request(request, id):
    booking = Booking.objects.get(id=id)
    booking.status = 'confirmed'
    booking.save()
    user = booking.user
    subject = "Service Request Approved"
    message = f"Dear {user.username}, your service request has been approved. You can now proceed with further steps. Please check your account for details. Thank you!"
    email_from = settings.EMAIL_HOST_USER
    email_to = [user.email]
    send_mail(subject, message, email_from, email_to)
    messages.success(request, "Booking request has been approved.", extra_tags='success')
    return redirect('designer_service_requests')

def reject_designer_request(request, id):
    booking = Booking.objects.get(id=id)
    booking.status = 'rejected'
    booking.save()
    user = booking.user
    subject = "Service Request Rejected"
    message = f"Dear {user.username}, we regret to inform you that your service request has been rejected. Please check your account for details or contact support for further assistance. Thank you!"
    email_from = settings.EMAIL_HOST_USER
    email_to = [user.email]
    send_mail(subject, message, email_from, email_to)
    messages.error(request, "Booking request has been rejected.", extra_tags='success')
    return redirect('designer_service_requests')
def start_designer_project(request, id):
    booking = Booking.objects.get(id=id)

    # Update status to "in_progress"
    booking.status = "in_progress"
    booking.save()

    # Send email notification
    subject = "Project Started"
    message = f"Dear {booking.user.username},\n\nYour project has started. You can track progress from your account.\n\nThank you!"
    email_from = settings.EMAIL_HOST_USER
    email_to = [booking.user.email]
    send_mail(subject, message, email_from, email_to)

    # Success message
    messages.success(request, "Project has been started.", extra_tags="success")

    return redirect('designer_service_request_detail', id=id)

def update_designer_booking_progress(request, id, progress):
    booking = Booking.objects.get(id=id)
    booking.progress = progress

    if progress == 25:
        booking.status = 'in_progress'
        status_message = "Your project has started and is now 25% complete."
    elif progress == 50:
        status_message = "Your project is now 50% complete. Progress is going smoothly!"
    elif progress == 75:
        status_message = "Your project is 75% complete. Almost done!"
    elif progress == 100:
        booking.status = 'completed'
        status_message = "Your project has been completed successfully. Thank you for choosing our service!"
    subject = "Project Progress Update"
    message = f"Dear {booking.user.username},\n\n{status_message}\n\nPlease check your account for details."
    email_from = settings.EMAIL_HOST_USER
    email_to = [booking.user.email]
    send_mail(subject, message, email_from, email_to)
    booking.save()
    messages.success(request, f"Booking progress updated to {progress}%.", extra_tags='success')

    return redirect('designer_service_request_detail', id=id)

def schedule_designer_project(request, id):
    booking = Booking.objects.get(id=id)
    if request.method == "POST":
        scheduled_date = request.POST.get("scheduled_date")
        if scheduled_date:
            booking.scheduled_date = scheduled_date
            booking.save()

            # Send email notification
            subject = "Project Scheduled"
            message = f"Dear {booking.user.username},\n\nYour project has been scheduled for {scheduled_date}.\n\nPlease be prepared for the work to begin on this date.\n\nThank you!"
            email_from = settings.EMAIL_HOST_USER
            email_to = [booking.user.email]
            send_mail(subject, message, email_from, email_to)

            messages.success(request, "Project scheduled successfully. An email has been sent to the client.", extra_tags="success")
        else:
            messages.error(request, "Please select a valid date.", extra_tags="error")

    return redirect('designer_service_request_detail', id=id)