from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw=False, **kwargs):
    if raw:
        return

    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, raw=False, **kwargs):
    if raw:
        return

    Profile.objects.get_or_create(user=instance)
    instance.profile.save()