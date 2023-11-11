# Generated by Django 3.2.18 on 2023-11-11 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letterapp', '0006_letter_received_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letter',
            name='is_checked',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='is_received',
        ),
        migrations.AddField(
            model_name='letter',
            name='state',
            field=models.CharField(choices=[('unchecked', '미확인'), ('checked', '확인 완료'), ('received', '저장 완료')], default='unchecked', max_length=20),
        ),
    ]