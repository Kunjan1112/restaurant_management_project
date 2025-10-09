from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# ------------------------------------MenuItems---------------------------------

# Create your models here.
class MenuItems(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    cuisine_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
              
# -------------------------------------------------------------------------------------

class MenuCategory(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# -------------------------------------------Review------------------------------------

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"

# ------------------------------------------Ingredient--------------------------------

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit_of_measure = models.CharField(max_length=50)

    def __str__(self):
        return self.name 