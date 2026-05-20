from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver


# Create your models here.
class Travel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Travel'
        verbose_name_plural = 'Travels'

    # def delete(self, *args, **kwargs):
    #     if self.places.filter(visited=True).exists():
    #         raise ValidationError('Travel have at least one visited place')
    #     return super().delete(*args, **kwargs)


@receiver(pre_delete, sender=Travel)
def delete_visited_places(sender, instance, **kwargs):
    if instance.places.filter(visited=True).exists():
        raise ValidationError('Travel have at least one visited place')


class Place(models.Model):
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    external_id = models.IntegerField(db_index=True)
    visited = models.BooleanField(default=False)
    travel = models.ForeignKey(to='Travel', on_delete=models.CASCADE, related_name='places')

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'
        unique_together = ('external_id', 'travel')

