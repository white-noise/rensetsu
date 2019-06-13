from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Kanji(models.Model):
    character      = models.CharField(max_length=10)
    alt_characters = models.CharField(max_length=10)
    radical        = models.CharField(max_length=10)
    strokes        = models.IntegerField()
    grade          = models.CharField(max_length=2)
    meaning        = models.TextField()
    reading_jpn    = models.CharField(max_length=100)   
    reading_eng    = models.CharField(max_length=100)

    def __str__(self):
        return self.character

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    interesting_kanji = models.ManyToManyField(Kanji, related_name="interesting_kanji")
    difficult_kanji   = models.ManyToManyField(Kanji, related_name="difficult_kanji")
    mastered_kanji    = models.ManyToManyField(Kanji, related_name="mastered_kanji")

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)