# Generated by Django 2.2.2 on 2019-07-19 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20190717_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='kanjireview',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
