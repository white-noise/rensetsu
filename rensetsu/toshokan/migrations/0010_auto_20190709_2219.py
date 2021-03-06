# Generated by Django 2.2.2 on 2019-07-09 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshokan', '0009_kanjicompound_frequency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kanji',
            name='alt_characters',
        ),
        migrations.RemoveField(
            model_name='kanji',
            name='meaning',
        ),
        migrations.RemoveField(
            model_name='kanji',
            name='radical',
        ),
        migrations.RemoveField(
            model_name='kanji',
            name='reading_eng',
        ),
        migrations.RemoveField(
            model_name='kanji',
            name='reading_jpn',
        ),
        migrations.AddField(
            model_name='kanji',
            name='jlpt',
            field=models.CharField(default='-', max_length=2),
        ),
        migrations.AddField(
            model_name='kanji',
            name='kun_meaning',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='kanji',
            name='on_meaning',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='kanji',
            name='reading',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='kanji',
            name='grade',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='kanji',
            name='strokes',
            field=models.IntegerField(default=0),
        ),
    ]
