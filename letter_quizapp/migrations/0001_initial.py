# Generated by Django 3.2.18 on 2023-11-30 02:08

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('letterapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter_quiz',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.TextField(max_length=300)),
                ('image', models.ImageField(blank=True, null=True, upload_to='letter_quiz/')),
                ('type', models.CharField(choices=[('choice', '객관식'), ('word', '단답형'), ('date', '날짜형')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('choice1', models.TextField(max_length=25, null=True)),
                ('choice2', models.TextField(max_length=25, null=True)),
                ('choice3', models.TextField(max_length=25, null=True)),
                ('choiceanswer', multiselectfield.db.fields.MultiSelectField(choices=[('choice1', '✓'), ('choice2', '✓'), ('choice3', '✓')], max_length=50, null=True)),
                ('wordanswer', models.TextField(max_length=15, null=True)),
                ('dateanswer', models.DateField(null=True)),
                ('letter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letter_quiz', to='letterapp.letter')),
            ],
        ),
    ]
