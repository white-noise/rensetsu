# Generated by Django 2.2.2 on 2019-07-27 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_kanjireview_is_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanjireviewobject',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
