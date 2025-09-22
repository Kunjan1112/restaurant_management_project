from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    if created:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if old_instance.status != instance.status:
        subject = f"Order #{instance.id} Status Updated"
        message = f"""

        Hello Admin,

        The status of Order #{instance.id} has changed.

        Old Status: {old_instance.status}
        New Status: {instance.status}

        Regards,
        Your Restaurant System
        """

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently = False,
        )