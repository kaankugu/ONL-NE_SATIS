from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ID = models.ManyToManyField(ID, on_delete=models.CASCADE)
    adress = models.ManyToManyField("Address")
    cards = models.ManyToManyField("cards")
    e_mail = models.EmailField( max_length=50)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField()
    permission = models.BooleanField(default=False)
    name = models.CharField( max_length=200)
    surname = models.CharField( max_length=200)
    
class Address(models.Model) : 
    Address_id = models.IntegerField( max_length = 24)
    address = models.CharField( max_length = 50)
    street = models.CharField( max_length = 50)
    city = models.CharField( max_length = 50)
    ilçe = models.CharField( max_length = 50)
       
class Cards(models.Model) : 
    cards_id =  models.IntegerField( max_length = 50)
    card_number = models.IntegerField( max_length = 50)
    cvs = models.IntegerField( max_length = 50)
    date = models.IntegerField( max_length = 50)



