from django.db import models

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

    def __str__(self):
        return self.name