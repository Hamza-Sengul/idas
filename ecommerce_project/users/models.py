# users/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone       = models.CharField(max_length=20, blank=True, verbose_name="Telefon Numarası")
    address     = models.TextField(blank=True, verbose_name="Adres")

    def __str__(self):
        return f"{self.user.username} Profil"


# Kullanıcı oluşturulduğunda otomatik Profile satırı oluşturmak için sinyal
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
