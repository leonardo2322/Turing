from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    image = models.ImageField(default='users/image_empty.png', upload_to="users/")
    location = models.CharField( max_length=80,null=True,blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ["-id"]


def creat_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()


post_save.connect(creat_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)