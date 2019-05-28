from django.db import models

class Kanji(models.Model):
	character      = models.CharField(max_length=10)
	alt_characters = models.CharField(max_length=10)
	radical        = models.CharField(max_length=10)
	strokes        = models.IntegerField()
	grade          = models.CharField(max_length=2)
	meaning        = models.TextField()
	reading        = models.CharField(max_length=30)