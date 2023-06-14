from django.db.models.signals import post_save, post_delete
from user_profiles.models import Profile


def update_user(sender, created, instance, **kwargs):
    """Update User's first name and last name when Profile is updated."""
    if not created:
        user = instance.user
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.email = instance.email
        user.save()


def delete_user(sender, instance, **kwargs):
    """Signal for deleting a user when a profile is deleted."""
    user = instance.user
    user.delete()


post_save.connect(update_user, sender=Profile)
post_delete.connect(delete_user, sender=Profile)
