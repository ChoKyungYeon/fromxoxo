# Generated by Django 3.2.18 on 2024-05-21 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0002_event_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='gift',
            field=models.TextField(max_length=2000, null=True),
        ),
    ]
