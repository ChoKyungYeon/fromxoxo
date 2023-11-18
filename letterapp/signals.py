from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import CustomUser, Letter

@receiver(pre_delete, sender=CustomUser)
def delete_user_letters(sender, instance, **kwargs):
    Letter.objects.filter(writer=instance, saver__isnull=True).delete()
    Letter.objects.filter(saver=instance, writer__isnull=True).delete()