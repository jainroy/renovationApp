from django import forms
from .models import *
from renovation_app.models import Register # type: ignore
from django.core.exceptions import ValidationError
import re
from django.core.validators import RegexValidator

class DesignerBookingForm(forms.ModelForm):

    class Meta:
        model = DesignerBooking
        fields = [
            'room_type', 
            'design_type', 
            'room_area', 
            'floor_type', 
            'wall_paint_color', 
            'ceiling_type', 
            'lighting_preference', 
            'description'
        ]

        widgets = {
            'design_type': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'floor_type': forms.Select(attrs={'class': 'form-control'}),
            'wall_paint_color': forms.Select(attrs={'class': 'form-control'}),
            'ceiling_type': forms.Select(attrs={'class': 'form-control'}),
            'lighting_preference': forms.Select(attrs={'class': 'form-control'}),
            'room_area': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ContractorBookingForm(forms.ModelForm):

    class Meta:
        model = ContractorBooking
        fields = [
            'project_type',
            'room_type', 
            'room_area', 
            'floor_type', 
            'wall_finish', 
            'ceiling_type', 
            'lighting_preference', 
            'budget_range',
            'description'
        ]

        widgets = {
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'floor_type': forms.Select(attrs={'class': 'form-control'}),
            'wall_finish': forms.Select(attrs={'class': 'form-control'}),
            'ceiling_type': forms.Select(attrs={'class': 'form-control'}),
            'lighting_preference': forms.Select(attrs={'class': 'form-control'}),
            'budget_range': forms.Select(attrs={'class': 'form-control'}),
            'room_area': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
