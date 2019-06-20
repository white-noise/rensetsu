from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from toshokan.models import Kanji

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    interesting_kanji = models.ManyToManyField(Kanji, 
    	blank=True, 
    	related_name="interesting_kanji")
    difficult_kanji   = models.ManyToManyField(Kanji, 
    	blank=True, 
    	related_name="difficult_kanji")
    known_kanji       = models.ManyToManyField(Kanji, 
    	blank=True, 
    	related_name="known_kanji")

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
