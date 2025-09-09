from django.db import models

class Home(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return self.title

class Feedback(models.Model):
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comments[:20]

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"{self.name} - ({self.email})"

class RestaurantLocation(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} - {self.zip_code}"

class Special(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.item_name

class OpeningHour(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday','Sunday'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES, unique=True)
    open_time = models.TimeField()
    close_time = models.TimeField()

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.day}: {self.open_time.strftime('%I:%M %p')} - {self.close_time.strftime('%I:%M %p')}"


class Chef(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='chefs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class NewSletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
 
class RestaurantInfo(models.Model):
    name = models.CharField(max_length=200, default="Delicious Bites Restaurant")
    city = models.CharField(max_length=100, default="Ahmedabad")
    address = models.TextField(default="123, SG Highway, Ahmedabad, Gujarat 380015")
    phone = models.CharField(max_length=20, default="+91 98765 43210")
    email = models.EmailField(blank=True, null=True)
    google_map_embed_url = models.TextField(
        default="https://www.google.com/maps/embed?pb=YOUR_MAP_URL"
    )

    hours = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),

    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(
        max_length = 20,
        choices = CATEGORY_CHOICES,
        default = 'main_course'
    )

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class ContactInfo(models.Model):
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.address} | {self.phone_number} | {self.email}"

