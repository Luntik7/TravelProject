from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Travel(models.Model):
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Travel'
        verbose_name_plural = 'Travels'


class Place(models.Model):
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    external_id = models.IntegerField()
    visited = models.BooleanField(default=False)
    travel = models.ForeignKey(to='Travel', on_delete=models.CASCADE, related_name='places')
    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'