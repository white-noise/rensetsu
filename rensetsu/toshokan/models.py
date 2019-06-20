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