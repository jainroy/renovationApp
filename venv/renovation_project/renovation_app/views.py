from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .forms import *
from django.conf import settings
from django.core.mail import send_mail
import secrets, string



def index(request):
    return render (request, 'index.html')
def single(request):
    return render (request, 'single.html')

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            data = Register.objects.filter(email = form.cleaned_data['email'])
            if data:
                messages.error(request, "User already exists!", extra_tags = "error")
                return redirect('user_login')
            if form.is_valid():
                user = form.save(commit = False)
                user.usertype = "user"
                user.password = make_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, "registration successful", extra_tags = "success")
                return redirect('user_login')
            else:
                messages.error(request, "Registration failed", extra_tags = "error")
                form = RegisterForm()
                return render (request, 'registration.html', {'form' : form, 'title': 'Register'})
    else:
        form = RegisterForm()
    return render (request, 'registration.html', {'form' : form, 'title': 'Register'})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                users = Register.objects.get(username = user)
                request.session['ut'] = users.usertype
                request.session['uid'] = users.id
                request.session['uname'] = users.username
                messages.success(request, "login successful", extra_tags = "success")
                return redirect('/')
            else:
                messages.error(request, "inavalid username or password", extra_tags = "error")
        else:
           messages.error(request, "Login failed", extra_tags = "error")
           form = LoginForm()
           return render(request, 'user_login.html', {'form' : form})
    else:
        form = LoginForm()
    return render(request,'user_login.html', {'form' : form})

def home(request):
    return render (request, 'home.html')

def registration_type(request):
    return render (request, 'registration_type.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Logout sucessful", extra_tags = "success")
    return redirect('/')

def view_users(request):
    users = Register.objects.filter(usertype="user")
    return render(request, 'users.html', {'users':users})
def view_designers(request):
    designers = Register.objects.filter(usertype="designer")
    return render(request, 'designers.html', {'designers':designers})
def view_contractors(request):
    contractors = Register.objects.filter(usertype="contractor")
    return render(request, 'contractors.html', {'contractors':contractors})

def profile(request):
    user = request.user
    id = Register.objects.get(id = user.id)
    return render (request, 'profile.html', {'user': user})



def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Prevent user from being logged out
            messages.success(request, "Profile updated successfully.", extra_tags="success")
            return redirect('profile') # Redirect to the profile page
        else:
            messages.error(request, "Profile update failed. Please check your form.", extra_tags = "error")
    else:
        form = UpdateProfileForm(instance=request.user)

    return render(request, 'registration.html', {'form': form, 'title':'Update'})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            data = Register.objects.filter(email=email)
            if data:
                new_password = generate_random_password()
                user=Register.objects.get(email=email)
                Reset.objects.create(otp=new_password,user=user)
                subject = "Password reset request"
                message = f'Your OTP is {new_password}'
                email_from = settings.EMAIL_HOST_USER
                email_to = [email]
                send_mail(subject, message, email_from, email_to)
                messages.success(request, 'OTP successfuly sent to your email', extra_tags = 'success')
                return redirect('reset_password')
            else:
                messages.error(request, 'Invalid email', extra_tags = 'error')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})
def generate_random_password(length = 6):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password
def reset_password(request):
    if request.method == 'POST':
        form=ResetPasswordForm(request.POST)
        if form.is_valid():
            otp=form.cleaned_data['otp']
            email=form.cleaned_data['email']
            user = Register.objects.get(email=email)
            user_otp=Reset.objects.filter(otp=otp).first()
            if user_otp.otp == otp:
                newpassword=form.cleaned_data['new_password']
                data=Register.objects.get(id=user.id)
                data.password=make_password(newpassword)
                data.save()

                user_otp.delete()

                messages.success(request,"Password changed", extra_tags="success")
                return redirect('user_login')
            else:
                print(1)
                messages.error(request,"Inavalid otp", extra_tags="error")
        else:
            print(2)
            messages.error(request,"Inavalid form data", extra_tags="error")
    else:
        print(3)
        form=ResetPasswordForm()
    return render(request,'reset_password.html',{'form':form})
def delete_user(request,id):
    user=Register.objects.get(id=id)
    subject="Account Deletion Notification"
    message=f"Dear {user.username} Your account is being deleted. You will no longer have access to your account. Please register again for future use..."
    email_from=settings.EMAIL_HOST_USER
    email_to=[user.email]
    send_mail(subject, message, email_from, email_to)

    user.delete()
    messages.success(request,'user deleted successfully',extra_tags='success')
    return redirect('view_users')

def designer_registration(request):
    if request.method == 'POST':
        form = DesignerRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            data = Register.objects.filter(email = form.cleaned_data['email'])
            if data:
                messages.error(request, "User already exists!", extra_tags = "error")
                return redirect('user_login')
            if form.is_valid():
                designer = form.save(commit = False)
                designer.usertype = "designer"
                designer.password = make_password(form.cleaned_data['password'])
                designer.save()
                messages.success(request, "Registration successful", extra_tags = "success")
                return redirect('user_login')
            else:
                messages.error(request, "Registration failed", extra_tags = "error")
                form = DesignerRegisterForm()
                return render (request, 'designer_registration.html', {'form' : form, 'title': 'Register'})
    else:
        form = DesignerRegisterForm()
    return render (request, 'designer_registration.html', {'form' : form, 'title': 'Register'})

def designer_profile(request):
    id = request.user.id
    designer = Register.objects.get(id=id)
    return render (request, 'designer_profile.html', {'designer': designer})

def update_designer_profile(request):
    user = Register.objects.get(id=request.user.id)  # Ensure correct user model instance
    if request.method == 'POST':
        form = UpdateDesignerProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)  # Prevent user from being logged out
            messages.success(request, "Profile updated successfully.", extra_tags="success")
            return redirect('designer_profile')  # Redirect to the profile page
        else:
            messages.error(request, "Profile update failed. Please check your form.", extra_tags="error")
    else:
        form = UpdateDesignerProfileForm(instance=user)

    return render(request, 'update_designer_profile.html', {'form': form, 'title': 'Update'})
def contractor_registration(request):
    if request.method == 'POST':
        form = ContractorRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            data = Register.objects.filter(email = form.cleaned_data['email'])
            if data:
                messages.error(request, "User already exists!", extra_tags = "error")
                return redirect('user_login')
            if form.is_valid():
                designer = form.save(commit = False)
                designer.usertype = "contractor"
                designer.password = make_password(form.cleaned_data['password'])
                designer.save()
                messages.success(request, "Registration successful", extra_tags = "success")
                return redirect('user_login')
            else:
                messages.error(request, "Registration failed", extra_tags = "error")
                form = DesignerRegisterForm()
                return render (request, 'contractor_registration.html', {'form' : form, 'title': 'Register'})
    else:
        form = DesignerRegisterForm()
    return render (request, 'contractor_registration.html', {'form' : form, 'title': 'Register'})

def contractor_profile(request):
    id = request.user.id
    contractor = Register.objects.get(id=id)
    return render (request, 'contractor_profile.html', {'contractor': contractor})

def update_contractor_profile(request):
    contractor = request.user
    print(contractor)
    user = Register.objects.get(id=contractor.id)  # Ensure correct user model instance
    if request.method == 'POST':
        form = UpdateContractorProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)  # Prevent user from being logged out
            messages.success(request, "Profile updated successfully.", extra_tags="success")
            return redirect('contractor_profile')  # Redirect to the profile page
        else:
            messages.error(request, "Profile update failed. Please check your form.", extra_tags="error")
    else:
        form = UpdateContractorProfileForm(instance=user)

    return render(request, 'update_contractor_profile.html', {'form': form, 'title': 'Update'})

def approve_designer(request,id):
    designer=Register.objects.get(id=id)
    subject="Account Approval Notification"
    message=f"Dear {designer.username} Your registration is being Approved. You can Login and continue using our services"
    email_from=settings.EMAIL_HOST_USER
    email_to=[designer.email]
    send_mail(subject, message, email_from, email_to)
    designer.is_approved=True
    designer.save()
    messages.success(request,'Designer approved successfully',extra_tags="success")
    return redirect('view_designers')


def reject_designer(request,id):
    designer=Register.objects.get(id=id)
    subject="Account Rejection Notification"
    message=f"Dear {designer.username} Your registration is being Rejected. Please register again with valid details for future use..."
    email_from=settings.EMAIL_HOST_USER
    email_to=[designer.email]
    send_mail(subject, message, email_from, email_to)
    designer.delete()
    messages.success(request,'Designer rejected successfully',extra_tags='success')
    return redirect('view_designers')

def delete_designer(request,id):
    designer=Register.objects.get(id=id)
    subject="Account Deletion Notification"
    message=f"Dear {designer.username} Your account is being deleted. You will no longer have access to your account. Please register again for future use..."
    email_from=settings.EMAIL_HOST_USER
    email_to=[designer.email]
    send_mail(subject, message, email_from, email_to)

    designer.delete()
    messages.success(request,'Designer deleted successfully',extra_tags='success')
    return redirect('view_designers')

def approve_contractor(request,id):
    contractor=Register.objects.get(id=id)
    subject="Account Approval Notification"
    message=f"Dear {contractor.username} Your registration is being Approved. You can Login and continue using our services"
    email_from=settings.EMAIL_HOST_USER
    email_to=[contractor.email]
    send_mail(subject, message, email_from, email_to)
    contractor.is_approved=True
    contractor.save()
    messages.success(request,'Contractor approved successfully',extra_tags="success")
    return redirect('view_contractors')


def reject_contractor(request,id):
    contractor=Register.objects.get(id=id)
    subject="Account Rejection Notification"
    message=f"Dear {contractor.username} Your registration is being Rejected. Please register again with valid details for future use..."
    email_from=settings.EMAIL_HOST_USER
    email_to=[contractor.email]
    send_mail(subject, message, email_from, email_to)
    contractor.delete()
    messages.success(request,'Designer rejected successfully',extra_tags='success')
    return redirect('view_contractors')

def delete_contractor(request,id):
    contractor=Register.objects.get(id=id)
    subject="Account Deletion Notification"
    message=f"Dear {contractor.username} Your account is being deleted. You will no longer have access to your account. Please register again for future use..."
    email_from=settings.EMAIL_HOST_USER
    email_to=[contractor.email]
    send_mail(subject, message, email_from, email_to)

    contractor.delete()
    messages.success(request,'Designer deleted successfully',extra_tags='success')
    return redirect('view_contractors')