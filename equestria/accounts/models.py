from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from colorfield.fields import ColorField


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_pony = models.CharField(max_length=1024, default="Tree Hugger")
    theme_choices = [
        (1, "Princess Luna"),  # Dark theme
        (2, "King Sombra"),  # Black/red theme
        (3, "Shining Armor"),  # Light/blue theme
        (4, "Pinkie Pie"),  # Overboard pink pony theme
    ]
    theme = models.IntegerField(choices=theme_choices, default=1)
    background_color = ColorField(default="#292929")
    background_lighter = ColorField(default="#373737")
    accent_color = ColorField(default="#18bc9c")
    accent_darker = ColorField(default="#1c613f")
    text_color = ColorField(default="#ffeeee")

    def __str__(self):
        return "{}'s profile".format(self.user)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
