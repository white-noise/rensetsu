# Generated by Django 3.0.6 on 2020-12-21 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toshokan', '0010_auto_20190709_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanjicompound',
            name='reading_jpn',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='kanjicompound',
            name='reading_eng',
            field=models.CharField(default='', max_length=100),
        ),
    ]
