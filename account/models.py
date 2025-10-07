from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

PREFERRED_CUISINE_CHOICES = (
    ('Italian', 'Italian'),
    ('Mexican', 'Mexican'),
    ('Asian', 'Asian'),
    ('Vegetarian', 'Vegetarian'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_cuisine = models.CharField(
        max_length = 50,
        choices = PREFERRED_CUISINE_CHOICES,
        null = True,
        blank = True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=user)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()