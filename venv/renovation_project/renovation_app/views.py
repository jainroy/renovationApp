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

def view_user(request):
    users = Register.objects.filter(usertype="user")
    return render(request, 'users.html', {'users':users})

def profile(request):
    user = request.user
    id = Register.objects.get(id = user.id)
    return render (request, 'profile.html', {'user': user})



def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Prevent user from being logged out
            messages.success(request, "Profile updated successfully.", extra_tags="success")
            return redirect('profile') # Redirect to the profile page
        else:
            messages.error(request, "Profile update failed. Please check your form.", extra_tags = "error")
    else:
        form = EditProfileForm(instance=request.user)

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
            user_otp=Reset.objects.filter(user=user).first()
            if user_otp.otp == otp:
                newpassword=form.cleaned_data['new_password']
                data=Register.objects.get(id=user.id)
                data.password=make_password(newpassword)
                data.save()

                user_otp.delete()

                messages.success(request,"Password changed", extra_tags="success")
                return redirect('user_login')
            else:
                messages.error(request,"Inavalid otp", extra_tags="error")
        else:
            messages.error(request,"Inavalid form data", extra_tags="error")
    else:
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
    return redirect('view_user')