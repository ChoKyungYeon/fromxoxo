# Generated by Django 3.2.18 on 2023-11-14 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documentapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='blog',
            new_name='bugreport',
        ),
        migrations.RemoveField(
            model_name='document',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='document',
            name='kakaotalk',
        ),
    ]