from django.db import models
from renovation_app.models import Register  # type: ignore # Importing the main User table

class DesignerBooking(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='user_bookings')  # Client booking the designer
    designer = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='designer_bookings')  # Designer being booked
    description = models.TextField(blank=True, null=True)  
    booking_date = models.DateTimeField(auto_now_add=True)  
    scheduled_date = models.DateField(blank=True, null=True)  

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)  # Default can be set in the form
    progress = models.IntegerField(default=0, help_text="Progress in percentage (0-100)")  # Default value for progress
    


    DESIGN_TYPE_CHOICES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('arabic', 'Arabic'),
        ('minimalist', 'Minimalist'),
        ('contemporary', 'Contemporary'),
        ('vintage', 'Vintage'),
        ('industrial', 'Industrial'),
        ('scandinavian', 'Scandinavian'),
        ('bohemian', 'Bohemian'),
        ('rustic', 'Rustic'),
        ('art deco', 'Art Deco'),
        ('mid century', 'Mid-Century'),
        ('transitional', 'Transitional'),
    ]

    ROOM_TYPE_CHOICES = [
        ('living_room', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('kitchen', 'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('office', 'Office'),
        ('shop', 'Shop'),
        ('hall', 'Hall'),
        ('entryway', 'Entryway'),
        ('laundry room', 'Laundry Room'),
        ('home theater', 'Home Theater'),
        ('library', 'Library'),
        ('garage', 'Garage'),
        ('gym', 'Gym'),
        ('playroom', 'Playroom'),
        ('study', 'Study'),
        ('balcony', 'Balcony'),
        ('terrace', 'Terrace'),
    ]

    FLOOR_TYPE_CHOICES = [
        ('tile', 'Tile'),
        ('marble', 'Marble'),
        ('wooden', 'Wooden'),
        ('vinyl', 'Vinyl'),
        ('laminate', 'Laminate'),
        ('carpet', 'Carpet'),
        ('bamboo', 'Bamboo'),
        ('concrete', 'Concrete'),
        ('cork', 'Cork'),
        ('terrazzo', 'Terrazzo'),
        ('stone', 'Stone'),
    ]
    WALL_PAINT_COLOR_CHOICES = [
        ('white', 'White'),
        ('off white', 'Off White'),
        ('beige', 'Beige'),
        ('gray', 'Gray'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
        ('purple', 'Purple'),
        ('orange', 'Orange'),
        ('brown', 'Brown'),
        ('black', 'Black'),
        ('custom', 'Custom'),
    ]

    CEILING_TYPE_CHOICES = [
        ('flat', 'Flat Ceiling'),
        ('vaulted', 'Vaulted Ceiling'),
        ('tray', 'Tray Ceiling'),
        ('coffered', 'Coffered Ceiling'),
        ('suspended', 'Suspended Ceiling'),
        ('beam', 'Beam Ceiling'),
        ('dome', 'Dome Ceiling'),
        ('custom', 'Custom Design'),
    ]

    LIGHTING_PREFERENCE_CHOICES = [
        ('warm white', 'Warm White'),
        ('cool white', 'Cool White'),
        ('daylight', 'Daylight'),
        ('ambient', 'Ambient Lighting'),
        ('task', 'Task Lighting'),
        ('accent', 'Accent Lighting'),
        ('chandelier', 'Chandelier'),
        ('recessed', 'Recessed Lighting'),
        ('pendant', 'Pendant Lighting'),
        ('wall_sconces', 'Wall Sconces'),
        ('floor_lamps', 'Floor Lamps'),
        ('table_lamps', 'Table Lamps'),
        ('custom', 'Custom Lighting'),
    ]


    # Room details
    design_type = models.CharField(max_length=50, choices=DESIGN_TYPE_CHOICES)  
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)  
    room_area = models.DecimalField(max_digits=6, decimal_places=2, help_text="Area in square feet")  
    floor_type = models.CharField(max_length=100, blank=True, null=True, choices=FLOOR_TYPE_CHOICES)  
    wall_paint_color = models.CharField(max_length=50, blank=True, null=True, choices=WALL_PAINT_COLOR_CHOICES)  
    ceiling_type = models.CharField(max_length=100, blank=True, null=True, choices=CEILING_TYPE_CHOICES)  
    lighting_preference = models.CharField(max_length=100, blank=True, null=True, choices=LIGHTING_PREFERENCE_CHOICES)  

class ContractorBooking(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='contractor_user_bookings')  # Client booking the contractor
    contractor = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='contractor_bookings')  # Contractor being booked
    description = models.TextField(blank=True, null=True)  
    booking_date = models.DateTimeField(auto_now_add=True)  
    scheduled_date = models.DateField(blank=True, null=True)  

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)  # Default can be set in the form
    progress = models.IntegerField(default=0, help_text="Progress in percentage (0-100)")  # Default value for progress
    
    PROJECT_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('renovation', 'Renovation'),
        ('landscaping', 'Landscaping'),
        ('infrastructure', 'Infrastructure'),
    ]

    ROOM_TYPE_CHOICES = [
        ('living_room', 'Living Room'),
        ('bedroom', 'Bedroom'),
        ('kitchen', 'Kitchen'),
        ('bathroom', 'Bathroom'),
        ('office', 'Office'),
        ('shop', 'Shop'),
        ('hall', 'Hall'),
        ('garage', 'Garage'),
        ('balcony', 'Balcony'),
        ('terrace', 'Terrace'),
    ]

    FLOOR_TYPE_CHOICES = [
        ('tile', 'Tile'),
        ('marble', 'Marble'),
        ('wooden', 'Wooden'),
        ('vinyl', 'Vinyl'),
        ('laminate', 'Laminate'),
        ('concrete', 'Concrete'),
    ]
    
    WALL_FINISH_CHOICES = [
        ('paint', 'Paint'),
        ('wallpaper', 'Wallpaper'),
        ('stone cladding', 'Stone Cladding'),
        ('wood paneling', 'Wood Paneling'),
        ('tiles', 'Tiles'),
    ]

    CEILING_TYPE_CHOICES = [
        ('flat', 'Flat Ceiling'),
        ('vaulted', 'Vaulted Ceiling'),
        ('tray', 'Tray Ceiling'),
        ('beam', 'Beam Ceiling'),
        ('custom', 'Custom Design'),
    ]

    LIGHTING_PREFERENCE_CHOICES = [
        ('warm white', 'Warm White'),
        ('cool white', 'Cool White'),
        ('daylight', 'Daylight'),
        ('chandelier', 'Chandelier'),
        ('recessed', 'Recessed Lighting'),
        ('pendant', 'Pendant Lighting'),
    ]
    
    BUDGET_RANGE_CHOICES = [
        ('low', 'Low Budget'),
        ('medium', 'Medium Budget'),
        ('high', 'High Budget'),
        ('luxury', 'Luxury'),
    ]

    # Project details
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)  
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES, blank=True, null=True)  
    room_area = models.DecimalField(max_digits=6, decimal_places=2, help_text="Area in square feet")  
    floor_type = models.CharField(max_length=100, blank=True, null=True, choices=FLOOR_TYPE_CHOICES)  
    wall_finish = models.CharField(max_length=50, blank=True, null=True, choices=WALL_FINISH_CHOICES)  
    ceiling_type = models.CharField(max_length=100, blank=True, null=True, choices=CEILING_TYPE_CHOICES)  
    lighting_preference = models.CharField(max_length=100, blank=True, null=True, choices=LIGHTING_PREFERENCE_CHOICES)  
    budget_range = models.CharField(max_length=50, choices=BUDGET_RANGE_CHOICES)