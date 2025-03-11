from django import forms
from .models import *
from renovation_app.models import Register # type: ignore
from django.core.exceptions import ValidationError
import re
from django.core.validators import RegexValidator
from .models import Booking, RoomDetails, DesignPreference, ContractPreference

class DesignerRoomForm(forms.ModelForm):
    class Meta:
        model = RoomDetails
        fields = ['room_type', 'room_area']
        widgets = {
            'room_area': forms.NumberInput(attrs={'step': '0.01'}),
        }

    design_type = forms.ChoiceField(choices=DesignPreference.DESIGN_TYPE_CHOICES, required=True)
    floor_type = forms.ChoiceField(choices=FLOOR_TYPE_CHOICES, required=True)
    wall_paint_color = forms.ChoiceField(choices=DesignPreference.WALL_PAINT_COLOR_CHOICES, required=True)
    ceiling_type = forms.ChoiceField(choices=CEILING_TYPE_CHOICES, required=True)
    lighting_preference = forms.ChoiceField(choices=LIGHTING_PREFERENCE_CHOICES, required=True)
    budget_range = forms.ChoiceField(choices=BUDGET_RANGE_CHOICES, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

DesignerRoomFormSet = forms.formset_factory(DesignerRoomForm, extra=1)

class ContractorRoomForm(forms.ModelForm):
    class Meta:
        model = RoomDetails
        fields = ['room_type', 'room_area']
        widgets = {
            'room_area': forms.NumberInput(attrs={'step': '0.01'}),
        }

    project_type = forms.ChoiceField(choices=ContractPreference.PROJECT_TYPE_CHOICES, required=True)
    floor_type = forms.ChoiceField(choices=FLOOR_TYPE_CHOICES, required=True)
    wall_finish = forms.ChoiceField(choices=ContractPreference.WALL_FINISH_CHOICES, required=True)
    ceiling_type = forms.ChoiceField(choices=CEILING_TYPE_CHOICES, required=True)
    lighting_preference = forms.ChoiceField(choices=LIGHTING_PREFERENCE_CHOICES, required=True)
    budget_range = forms.ChoiceField(choices=BUDGET_RANGE_CHOICES, required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

ContractorRoomFormSet = forms.formset_factory(ContractorRoomForm, extra=1)

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message', 'rating']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your feedback'}),
            'rating': forms.HiddenInput(),  # We will use stars instead of a dropdown
        }
