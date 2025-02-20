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
        ('art_deco', 'Art Deco'),
        ('mid_century', 'Mid-Century'),
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
        ('laundry_room', 'Laundry Room'),
        ('home_theater', 'Home Theater'),
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
        ('off_white', 'Off White'),
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
        ('warm_white', 'Warm White'),
        ('cool_white', 'Cool White'),
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

