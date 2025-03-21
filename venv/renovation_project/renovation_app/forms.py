from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re
from .models import Register
from django.core.validators import RegexValidator


class RegisterForm(forms.ModelForm):
    confirm_password=forms.CharField(
        max_length=20,
        label="CONFIRM PASSWORD",
        required=True,
        widget=forms.PasswordInput(attrs={'id':'confirm_password','name':'confirm_password'})
    )
    
    class Meta:
        model=Register
        fields=['first_name','last_name','username','email','contact','password']
        widgets={
            'first_name':forms.TextInput(attrs={'id':'first_name','name':'first_name'}),
            'last_name':forms.TextInput(attrs={'id':'last_name','name':'last_name'}),
            'username':forms.TextInput(attrs={'id':'username','name':'username'}),
            'email':forms.EmailInput(attrs={'id':'email','name':'email',}),
            'contact':forms.TextInput(attrs={'id':'contact','name':'contact'}),
            'password':forms.PasswordInput(attrs={'id':'password','name':'password'}),
        }
        labels={
            'first_name':'FIRST NAME',
            'last_name':'LAST NAME',
            'username':'USERNAME',
            'email':'EMAIL',
            'contact':'CONTACT NUMBER',
            'password':'PASSWORD'
        }
        help_texts={
            'username':None
        }
   
    # Custom Validation for username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        if not username.isalnum():
            raise ValidationError("Username must only contain alphanumeric characters.")
        # Check if the username already exists (assuming you have a model named Register)
        if Register.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
    
    
    
    # Custom Validation for contact
    def clean_contact(self):
        contact = str(self.cleaned_data.get('contact'))  # Ensure contact is a string
        if len(contact) != 10:
            raise ValidationError("Contact number must be exactly 10 digits.")
        if not contact.isdigit():
            raise ValidationError("Contact number must contain only digits.")
        return contact
    
    # Custom Validation for password
    def clean_password(self):
        password = self.cleaned_data.get('password')
         # Only validate if password is required
        if self.fields['password'].required:
            if len(password) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if not re.search(r'\d', password):
                raise ValidationError("Password must contain at least one digit.")
            if not re.search(r'[A-Za-z]', password):
                raise ValidationError("Password must contain at least one letter.")
        return password
        
    
    # Custom Validation for confirm_password
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise ValidationError("Passwords do not match.")
        return confirm_password


    

class LoginForm(forms.Form):
    username=forms.CharField(
        max_length=50,
        label="USERNAME",
        widget=forms.TextInput(attrs={'id':'username','name':'username'})
    )
    password=forms.CharField(
        max_length=20,
        label="PASSWORD",
        widget=forms.PasswordInput(attrs={'id':'password','name':'password'})
    )
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=Register
        fields=['first_name', 'last_name', 'username', 'email', 'contact', 'image']
        widgets={
            'first_name':forms.TextInput(attrs={'id':'first_name','name':'first_name'}),
            'last_name':forms.TextInput(attrs={'id':'last_name','name':'last_name'}),
            'username':forms.TextInput(attrs={'id':'username','name':'username'}),
            'email':forms.EmailInput(attrs={'id':'email','name':'email',}),
            'contact':forms.TextInput(attrs={'id':'contact','name':'contact'}),
            'image':forms.FileInput(attrs={'id':'image','name':'image'}),
        }
        labels={
            'first_name':'FIRST NAME',
            'last_name':'LAST NAME',
            'username':'USERNAME',
            'email':'EMAIL',
            'contact':'CONTACT NUMBER',
            'image':'PROFILE PICTURE',
        }
        help_texts={
            'username': None
        }
    # Custom Validation for username
    def clean_username(self):
            username = self.cleaned_data.get('username')
            if len(username) < 5:
                raise ValidationError("Username must be at least 5 characters long.")
            if not username.isalnum():
                raise ValidationError("Username must only contain alphanumeric characters.")
            # Check if the username already exists (assuming you have a model named Register)
            if Register.objects.filter(username=username).exclude(id=self.instance.id).exists():
                raise ValidationError("This username is already taken.")

            return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Register.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError("An account with this email already exists.")
        return email
    
    # Custom Validation for contact
    def clean_contact(self):
        contact = str(self.cleaned_data.get('contact')) # Ensure contact is a string
        if len(contact) != 10:
            raise ValidationError("Contact number must be exactly 10 digits.")
        if not contact.isdigit():
            raise ValidationError("Contact number must contain only digits.")
        return contact
    
class ForgotPasswordForm(forms.Form):
    email = forms.CharField(max_length = 50, label = "Email", widget = forms.EmailInput(attrs = { 'name': 'email', 'id' : 'email'}))

class ResetPasswordForm(forms.Form):
    otp = forms.CharField(max_length = 6, label = "OTP", widget = forms.TextInput(attrs = { 'name': 'otp', 'id' : 'otp'}))
    email = forms.CharField(max_length = 50, label = "Email", widget = forms.EmailInput(attrs = { 'name': 'email', 'id' : 'email'}))
    new_password = forms.CharField(max_length = 50, label = "New Password", widget = forms.PasswordInput(attrs = { 'name': 'new_password', 'id' : 'new_password'}))
    confirm_password = forms.CharField(max_length = 50, label = "Confirm Password", widget = forms.PasswordInput(attrs = { 'name': 'confirm_password', 'id' : 'confirm_password'}))


# from django import forms
# from django.core.exceptions import ValidationError
# import re
# from .models import Register  # Assuming you have a Register model

class DesignerRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=20,
        label="CONFIRM PASSWORD",
        required=True,
        widget=forms.PasswordInput(attrs={'id': 'confirm_password', 'name': 'confirm_password'})
    )

    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'username', 'email', 'contact', 'license_no', 'experience', 'password', 'confirm_password']
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'name': 'first_name'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'name': 'last_name'}),
            'username': forms.TextInput(attrs={'id': 'username', 'name': 'username'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'name': 'email'}),
            'contact': forms.TextInput(attrs={'id': 'contact', 'name': 'contact'}),
            'license_no': forms.TextInput(attrs={'id': 'license_no', 'name': 'license_no'}),
            'experience': forms.NumberInput(attrs={'id': 'experience', 'name': 'experience'}),
            'password': forms.PasswordInput(attrs={'id': 'password', 'name': 'password'}),
        }
        labels = {
            'first_name': 'FIRST NAME',
            'last_name': 'LAST NAME',
            'username': 'USERNAME',
            'email': 'EMAIL',
            'contact': 'CONTACT NUMBER',
            'license_no': 'LICENSE NO',
            'experience': 'EXPERIENCE',
            'password': 'PASSWORD',
            'confirm_password': 'CONFIRM PASSWORD'
        }
        help_texts = {
            'username': None
        }

    # Custom Validation for username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        if not username.isalnum():
            raise ValidationError("Username must only contain alphanumeric characters.")
        if Register.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    # Custom Validation for contact
    def clean_contact(self):
        contact = str(self.cleaned_data.get('contact'))
        if len(contact) != 10 or not contact.isdigit():
            raise ValidationError("Contact number must be exactly 10 digits and contain only numbers.")
        return contact

    # Custom Validation for license number
    def clean_license_no(self):
        license_no = str(self.cleaned_data.get('license_no')).strip()
        pattern = r"^CA/\d{4}/\d{5}$"
        if not re.match(pattern, license_no):
            raise ValidationError("License number must be in the format 'CA/YYYY/XXXXX' (e.g., 'CA/2024/23456').")
        return license_no

    # Custom Validation for password
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Za-z]', password):
            raise ValidationError("Password must be at least 8 characters long, contain at least one digit, and one letter.")
        return password

    # Custom Validation for confirm_password
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise ValidationError("Passwords do not match.")
        return confirm_password

class UpdateDesignerProfileForm(forms.ModelForm):
    SPECIALIZATION_CHOICES = [
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
        ('Hospitality', 'Hospitality'),
        ('Retail', 'Retail'),
        ('Healthcare', 'Healthcare'),
        ('Landscape', 'Landscape'),
        ('Industrial', 'Industrial'),
        ('Office', 'Office'),
        ('Sustainable', 'Sustainable'),
        ('Lighting', 'Lighting'),
    ]

    specialization = forms.ChoiceField(
        choices=SPECIALIZATION_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'id': 'specialization', 'name': 'specialization'})
    )

    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'username', 'email', 'contact', 'license_no', 'experience', 'image', 'location', 'specialization', 'portfolio']
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'name': 'first_name'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'name': 'last_name'}),
            'username': forms.TextInput(attrs={'id': 'username', 'name': 'username'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'name': 'email'}),
            'contact': forms.TextInput(attrs={'id': 'contact', 'name': 'contact'}),
            'license_no': forms.TextInput(attrs={'id': 'license_no', 'name': 'license_no'}),
            'experience': forms.NumberInput(attrs={'id': 'experience', 'name': 'experience'}),
            'image': forms.FileInput(attrs={'id': 'image', 'name': 'image'}),
            'location': forms.URLInput(attrs={'id': 'location', 'name': 'location'}),
            'portfolio': forms.FileInput(attrs={'id': 'portfolio', 'name': 'portfolio', 'accept': 'application/pdf'}),
        }
        labels = {
            'first_name': 'FIRST NAME',
            'last_name': 'LAST NAME',
            'username': 'USERNAME',
            'email': 'EMAIL',
            'contact': 'CONTACT NUMBER',
            'license_no': 'LICENSE NO',
            'experience': 'EXPERIENCE',
            'image': 'NEW PROFILE PICTURE',
            'location': 'GOOGLE MAPS LOCATION',
            'specialization': 'SPECIALIZATION',
            'portfolio': 'UPDATED PORTFOLIO',
        }
        help_texts = {
            'username': None
        }
        # Custom Validation for contact
    def clean_contact(self):
        contact = str(self.cleaned_data.get('contact'))
        if len(contact) != 10 or not contact.isdigit():
            raise ValidationError("Contact number must be exactly 10 digits and contain only numbers.")
        return contact

    # Custom Validation for license number
    def clean_license_no(self):
        license_no = str(self.cleaned_data.get('license_no')).strip()
        pattern = r"^CA/\d{4}/\d{5}$"
        if not re.match(pattern, license_no):
            raise ValidationError("License number must be in the format 'CA/YYYY/XXXXX' (e.g., 'CA/2024/23456').")
        return license_no
    def clean_portfolio(self):
        portfolio = self.cleaned_data.get('portfolio')
        if portfolio:
            if not portfolio.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
        return portfolio
class ContractorRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=20,
        label="CONFIRM PASSWORD",
        required=True,
        widget=forms.PasswordInput(attrs={'id': 'confirm_password', 'name': 'confirm_password'})
    )

    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'username', 'email', 'contact', 'license_no', 'experience', 'password', 'confirm_password']
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'name': 'first_name'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'name': 'last_name'}),
            'username': forms.TextInput(attrs={'id': 'username', 'name': 'username'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'name': 'email'}),
            'contact': forms.TextInput(attrs={'id': 'contact', 'name': 'contact'}),
            'license_no': forms.TextInput(attrs={'id': 'license_no', 'name': 'license_no'}),
            'experience': forms.NumberInput(attrs={'id': 'experience', 'name': 'experience'}),
            'password': forms.PasswordInput(attrs={'id': 'password', 'name': 'password'}),
        }
        labels = {
            'first_name': 'FIRST NAME',
            'last_name': 'LAST NAME',
            'username': 'USERNAME',
            'email': 'EMAIL',
            'contact': 'CONTACT NUMBER',
            'license_no': 'LICENSE NO',
            'experience': 'EXPERIENCE',
            'password': 'PASSWORD',
            'confirm_password': 'CONFIRM PASSWORD'
        }
        help_texts = {
            'username': None
        }

    # Custom Validation for username
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise ValidationError("Username must be at least 5 characters long.")
        if not username.isalnum():
            raise ValidationError("Username must only contain alphanumeric characters.")
        if Register.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    # Custom Validation for contact
    def clean_contact(self):
        contact = str(self.cleaned_data.get('contact'))
        if len(contact) != 10 or not contact.isdigit():
            raise ValidationError("Contact number must be exactly 10 digits and contain only numbers.")
        return contact

    # Custom Validation for license number
    def clean_license_no(self):
        license_no = str(self.cleaned_data.get('license_no')).strip()
        pattern = r"^[A-Z]{2}/[A-Z]+/[A-Z]+/\d{4}/\d{5}$"
        
        if not re.match(pattern, license_no):
            raise ValidationError(
                "Invalid format! License number must be in the format '[State Code]/[Department]/[Category]/[Year]/[Serial Number]' "
                "(e.g., 'MH/PWD/CON/2024/00123')."
            )
        
        return license_no

    # Custom Validation for password
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Za-z]', password):
            raise ValidationError("Password must be at least 8 characters long, contain at least one digit, and one letter.")
        return password

    # Custom Validation for confirm_password
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if confirm_password != password:
            raise ValidationError("Passwords do not match.")
        return confirm_password

class UpdateContractorProfileForm(forms.ModelForm):
    CONTRACTOR_SPECIALIZATION_CHOICES = [
        ('General Contractor', 'General Contractor'),
        ('Residential Construction', 'Residential Construction'),
        ('Commercial Construction', 'Commercial Construction'),
        ('Renovation & Remodeling', 'Renovation & Remodeling'),
        ('Masonry & Brickwork', 'Masonry & Brickwork'),
        ('Plumbing', 'Plumbing'),
        ('Electrical', 'Electrical'),
        ('Carpentry & Woodwork', 'Carpentry & Woodwork'),
        ('Painting & Finishing', 'Painting & Finishing'),
        ('Roofing & Waterproofing', 'Roofing & Waterproofing'),
        ('Flooring & Tiling', 'Flooring & Tiling'),
        ('HVAC & Ventilation', 'HVAC & Ventilation'),
        ('Steel & Structural Work', 'Steel & Structural Work'),
        ('Glass & Aluminum Work', 'Glass & Aluminum Work'),
        ('False Ceiling & Partition', 'False Ceiling & Partition'),
        ('Modular Kitchen & Furniture', 'Modular Kitchen & Furniture'),
    ]

    specialization = forms.ChoiceField(
        choices=CONTRACTOR_SPECIALIZATION_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'id': 'specialization', 'name': 'specialization'})
    )

    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'username', 'email', 'contact', 'license_no', 'experience', 'image', 'location', 'specialization', 'portfolio']
        widgets = {
            'first_name': forms.TextInput(attrs={'id': 'first_name', 'name': 'first_name'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name', 'name': 'last_name'}),
            'username': forms.TextInput(attrs={'id': 'username', 'name': 'username'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'name': 'email'}),
            'contact': forms.TextInput(attrs={'id': 'contact', 'name': 'contact'}),
            'license_no': forms.TextInput(attrs={'id': 'license_no', 'name': 'license_no'}),
            'experience': forms.NumberInput(attrs={'id': 'experience', 'name': 'experience'}),
            'image': forms.FileInput(attrs={'id': 'image', 'name': 'image'}),
            'location': forms.URLInput(attrs={'id': 'location', 'name': 'location'}),
            'portfolio': forms.FileInput(attrs={'id': 'portfolio', 'name': 'portfolio', 'accept': 'application/pdf'}),
        }
        labels = {
            'first_name': 'FIRST NAME',
            'last_name': 'LAST NAME',
            'username': 'USERNAME',
            'email': 'EMAIL',
            'contact': 'CONTACT NUMBER',
            'license_no': 'LICENSE NO',
            'experience': 'EXPERIENCE',
            'image': 'NEW PROFILE PICTURE',
            'location': 'GOOGLE MAPS LOCATION',
            'specialization': 'SPECIALIZATION',
            'portfolio': 'UPDATED PORTFOLIO',
        }
        help_texts = {
            'username': None
        }
        # Custom Validation for contact
    def clean_contact(self):
        contact = str(self.cleaned_data.get('contact'))
        if len(contact) != 10 or not contact.isdigit():
            raise ValidationError("Contact number must be exactly 10 digits and contain only numbers.")
        return contact

    # Custom Validation for license number
    def clean_license_no(self):
        license_no = str(self.cleaned_data.get('license_no')).strip()
        pattern = r"^[A-Z]{2}/[A-Z]+/[A-Z]+/\d{4}/\d{5}$"
        
        if not re.match(pattern, license_no):
            raise ValidationError(
                "Invalid format! License number must be in the format '[State Code]/[Department]/[Category]/[Year]/[Serial Number]' "
                "(e.g., 'MH/PWD/CON/2024/00123')."
            )
        return license_no
    def clean_portfolio(self):
        portfolio = self.cleaned_data.get('portfolio')
        if portfolio:
            if not portfolio.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
        return portfolio
