# Generated by Django 2.2.2 on 2019-07-19 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_kanjireview_is_complete'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanjireviewobject',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]