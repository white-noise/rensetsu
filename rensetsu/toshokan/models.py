from django.db import models
from django.contrib.auth.models import User

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

class KanjiCompound(models.Model):
    characters        = models.CharField(max_length=20)
    meaning           = models.TextField()
    frequency         = models.IntegerField(default=0, blank=True)
    # reading_jpn       = models.CharField(max_length=100)   
    reading_eng       = models.CharField(max_length=100)
    constituent_kanji = models.ManyToManyField(Kanji, 
        blank=True, 
        related_name="constituent_kanji", 
        through="KanjiCompoundElement")

    def __str__(self):
        return self.characters

class KanjiCompoundElement(models.Model):
    kanji_compound = models.ForeignKey(KanjiCompound, on_delete=models.CASCADE)
    kanji          = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    position       = models.IntegerField()
    # shared frequency for this particular jukugo to reference in sorting

    def __str__(self):
        return self.kanji_compound.characters