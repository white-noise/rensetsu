# Generated by Django 2.2.2 on 2019-07-02 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toshokan', '0007_auto_20190701_2230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kanjicompound',
            name='reading_jpn',
        ),
    ]