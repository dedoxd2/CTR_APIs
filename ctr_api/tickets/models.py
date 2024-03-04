from django.db import models


from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User

# Guest -- Movie -- Reservation 

class Moive (models.Model):

    hall = models.CharField(max_length=10 )
    movie=  models.CharField(max_length=10 )
    date = models.DateField()

    def __str__(self):
        return self.movie



class Guest(models.Model):
    name =  models.CharField(max_length=10 )
    mobile = models.CharField(max_length=10 )

    def __str__ (self):
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(Guest,related_name="reservation" , on_delete=models.CASCADE)
    moive = models.ForeignKey(Moive,related_name="reservation", on_delete=models.CASCADE)


    def __str__(self):
        return str(self.pk)


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length = 50)
    body =  models.TextField()

    def __str__(self,):
        return self.title


@receiver(post_save , sender = settings.AUTH_USER_MODEL)
def CreateToken(sender,instance,created, **kwargs):
    if created:
        Token.objects.create(user=instance)