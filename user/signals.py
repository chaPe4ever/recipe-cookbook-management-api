from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from author.models import Author
from registration_profile.models import RegistrationProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_registration_profile(sender, instance, created, **kwargs):
    # Create registration profile for new users
    if created:
        RegistrationProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_author_profile(sender, instance, created, **kwargs):
    if created:
        # Create author profile
        Author.objects.create(user=instance)
        # Automatically add new users to 'Authors' group
        authors_group, _ = Group.objects.get_or_create(name="Authors")
        instance.groups.add(authors_group)
