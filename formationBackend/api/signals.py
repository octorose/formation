from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Personnel, Group  

@receiver(post_save, sender=Personnel)
def update_effectif_on_save(sender, instance, **kwargs):
    if instance.group:
        group = instance.group
        group.Effectif = Personnel.objects.filter(group=group).count()
        group.save()

@receiver(post_delete, sender=Personnel)
def update_effectif_on_delete(sender, instance, **kwargs):
    if instance.group:
        group = instance.group
        group.Effectif = Personnel.objects.filter(group=group).count()
        group.save()
