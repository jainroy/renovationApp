from django.db import models
from renovation_app.models import Register  # type: ignore # Main User table

# Common choices reused across models
FLOOR_TYPE_CHOICES = [
    ('', '---------'),
    ('tile', 'Tile'),
    ('marble', 'Marble'),
    ('wooden', 'Wooden'),
    ('vinyl', 'Vinyl'),
    ('laminate', 'Laminate'),
    ('concrete', 'Concrete'),
]

CEILING_TYPE_CHOICES = [
    ('', '---------'),
    ('flat', 'Flat Ceiling'),
    ('vaulted', 'Vaulted Ceiling'),
    ('tray', 'Tray Ceiling'),
    ('beam', 'Beam Ceiling'),
    ('custom', 'Custom Design'),
]

LIGHTING_PREFERENCE_CHOICES = [
    ('', '---------'),
    ('warm white', 'Warm White'),
    ('cool white', 'Cool White'),
    ('daylight', 'Daylight'),
    ('chandelier', 'Chandelier'),
    ('recessed', 'Recessed Lighting'),
    ('pendant', 'Pendant Lighting'),
]
BUDGET_RANGE_CHOICES = [
    ('', '---------'),
    ('low', 'Low Budget'),
    ('medium', 'Medium Budget'),
    ('high', 'High Budget'),
    ('luxury', 'Luxury'),
]

class Booking(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='user_bookings')  # Client
    designer = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='designer_bookings', null=True, blank=True)  # Designer
    contractor = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='contractor_bookings', null=True, blank=True)  # Contractor
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
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    progress = models.IntegerField(default=0, help_text="Progress in percentage (0-100)")

    def __str__(self):
        rooms = ", ".join([room.room_type for room in self.rooms.all()])
        return f"Booking for {rooms} - {self.user}" if rooms else f"Booking - {self.user}"

class RoomDetails(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='rooms', null=True)
    room_type = models.CharField(max_length=50, choices=[
        ('', '---------'),
        ('living room', 'Living Room'),
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
    ])
    room_area = models.DecimalField(max_digits=6, decimal_places=2, help_text="Area in square feet")
    design_preference = models.ForeignKey('DesignPreference', on_delete=models.SET_NULL, null=True, blank=True)
    contract_preference = models.ForeignKey('ContractPreference', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.room_type} - {self.room_area} sqft"

class DesignPreference(models.Model):
    DESIGN_TYPE_CHOICES = [
        ('', '---------'),
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

    WALL_PAINT_COLOR_CHOICES = [
        ('', '---------'),
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

    design_type = models.CharField(max_length=50, choices=[('', '---------')] + DESIGN_TYPE_CHOICES)
    floor_type = models.CharField(max_length=100, blank=True, null=True, choices=[('', '---------')] + FLOOR_TYPE_CHOICES)
    wall_paint_color = models.CharField(max_length=50, blank=True, null=True, choices=[('', '---------')] + WALL_PAINT_COLOR_CHOICES)
    ceiling_type = models.CharField(max_length=100, blank=True, null=True, choices=[('', '---------')] + CEILING_TYPE_CHOICES)
    lighting_preference = models.CharField(max_length=100, blank=True, null=True, choices=[('', '---------')] + LIGHTING_PREFERENCE_CHOICES)
    budget_range = models.CharField(max_length=50, choices=[('', '---------')] + BUDGET_RANGE_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.design_type} Design"

class ContractPreference(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('', '---------'),
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('renovation', 'Renovation'),
        ('landscaping', 'Landscaping'),
        ('infrastructure', 'Infrastructure'),
    ]

    WALL_FINISH_CHOICES = [
        ('', '---------'),
        ('paint', 'Paint'),
        ('wallpaper', 'Wallpaper'),
        ('stone cladding', 'Stone Cladding'),
        ('wood paneling', 'Wood Paneling'),
        ('tiles', 'Tiles'),
    ]

    project_type = models.CharField(max_length=50, choices=[('', '---------')] + PROJECT_TYPE_CHOICES)
    floor_type = models.CharField(max_length=100, blank=True, null=True, choices=[('', '---------')] + FLOOR_TYPE_CHOICES)
    wall_finish = models.CharField(max_length=50, blank=True, null=True, choices=[('', '---------')] + WALL_FINISH_CHOICES)
    ceiling_type = models.CharField(max_length=100, blank=True, null=True, choices=[('', '---------')] + CEILING_TYPE_CHOICES)
    lighting_preference = models.CharField(max_length=100, blank=True, null=True, choices=[('', '---------')] + LIGHTING_PREFERENCE_CHOICES)
    budget_range = models.CharField(max_length=50, choices=[('', '---------')] + BUDGET_RANGE_CHOICES)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.project_type} Contract Work"
    

class Feedback(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,related_name="booking")  # Linking feedback to a user
    user = models.ForeignKey(Register,on_delete=models.CASCADE,related_name="user_feed")  # Linking feedback to a user
    designer = models.ForeignKey(Register,on_delete=models.CASCADE,null=True,related_name="designer_feedback")
    message = models.TextField(max_length=500,null=True)  # Feedback content
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when feedback was created

    def _str_(self):
        return f"Feedback from {self.user.username} - {self.rating} stars"