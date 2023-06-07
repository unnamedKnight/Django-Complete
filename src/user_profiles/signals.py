from django.db.models.signals import post_save, post_delete
from user_profiles.models import Profile



def delete_user(sender, instance, **kwargs):
    """Signal for deleting a user when a profile is deleted."""
    user = instance.user
    user.delete()


post_delete.connect(delete_user, sender=Profile)