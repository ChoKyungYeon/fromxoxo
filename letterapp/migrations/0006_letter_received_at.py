# Generated by Django 3.2.18 on 2023-11-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letterapp', '0005_letter_is_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='received_at',
            field=models.DateTimeField(null=True),
        ),
    ]