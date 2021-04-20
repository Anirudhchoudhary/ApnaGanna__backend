from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from sound.models import Sound


# Create your models here.
User = get_user_model()


def gettoken(sender , instance , **kwargs):
    refresh = RefreshToken.for_user(instance)
    if(refresh):
        u = UserProfile.objects.create(user = instance , jwtrefresh=str(refresh) , jwtaccess=str(refresh.access_token))
        u.save()
        print("user new JWT is created")
    

    

class UserProfile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    ip_addr = models.CharField(max_length=300 , null = True , blank=True)
    jwtrefresh = models.CharField(max_length=300 , null = True , blank=True)
    jwtaccess = models.CharField(max_length=300 , null = True , blank=True)
    songlike = models.ManyToManyField(Sound , blank=True)
    playlist = models.ManyToManyField(Sound , blank=True , related_name="playlist")
    
    def __str__(self):
        return self.user.username



post_save.connect(gettoken , sender=User)