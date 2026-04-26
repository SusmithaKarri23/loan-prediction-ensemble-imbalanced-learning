from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def update_admin_user_type(sender, instance, created, **kwargs):
    """Automatically set user_type to 'admin' if user is superuser"""
    if instance.is_superuser and instance.user_type != 'admin':
        User.objects.filter(pk=instance.pk).update(user_type='admin')
    elif not instance.is_superuser and instance.user_type == 'admin':
        User.objects.filter(pk=instance.pk).update(user_type='user')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create UserProfile when User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
