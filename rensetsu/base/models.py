from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from toshokan.models import Kanji
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    interesting_kanji = models.ManyToManyField(Kanji, blank=True, related_name="interesting_kanji")
    difficult_kanji   = models.ManyToManyField(Kanji, blank=True, related_name="difficult_kanji")
    known_kanji       = models.ManyToManyField(Kanji, blank=True, related_name="known_kanji")

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class KanjiGroup(models.Model):
    name        = models.CharField(max_length=100)
    user        = models.ForeignKey(UserProfile, related_name="group_profile", on_delete=models.CASCADE)
    group_kanji = models.ManyToManyField(Kanji, blank=True, related_name="group_kanji", through="KanjiGroupElement")
    date_time   = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)

class KanjiGroupElement(models.Model):
    kanji     = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    group     = models.ForeignKey(KanjiGroup, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)

class KanjiComment(models.Model):
    kanji     = models.ForeignKey(Kanji, related_name="kanji_comment", on_delete=models.CASCADE)
    user      = models.ForeignKey(UserProfile, related_name="comment_profile", on_delete=models.CASCADE)
    comment   = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.comment)

class KanjiReview(models.Model):
    user      = models.ForeignKey(UserProfile, related_name="reviews", on_delete=models.CASCADE)
    group     = models.ForeignKey(KanjiGroup, related_name="reviews", on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ("review_%s"%(self.group.name))

class KanjiReviewObject(models.Model):
    kanji  = models.ForeignKey(Kanji, related_name="review_objects", on_delete=models.CASCADE)
    review = models.ForeignKey(KanjiReview, related_name="review_objects", on_delete=models.CASCADE)
    score  = models.IntegerField(default=0)

    def __str__(self):
        return ("review_kanji_%s"%(self.kanji.character))

class KanjiReviewObjectOption(models.Model):

    review_object = models.ForeignKey(KanjiReviewObject, related_name="options", on_delete=models.CASCADE, null=True)
    possible_response = models.CharField(max_length=500)
    response_correct = models.BooleanField(default=False)

    def __str__(self):
        return ("review_option_%s"%(self.possible_response))

