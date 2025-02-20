from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re
from .models import Register
from django.core.validators import RegexValidator


