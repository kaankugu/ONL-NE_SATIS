from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    #adress = models.ManyToManyField(Address,on_delete=...)
    adress = models.ManyToManyField("Address")
    cards = models.ManyToManyField("cards")
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    permission = models.BooleanField(default=False)
    
class Address(models.Model) : 
    Address_id = models.IntegerField( )
    address = models.CharField( max_length = 50)
    street = models.CharField( max_length = 50)
    city = models.CharField( max_length = 50)
    ilçe = models.CharField( max_length = 50)
       
class Cards(models.Model) : 
    cards_id =  models.IntegerField()
    card_number = models.IntegerField()
    cvs = models.IntegerField()
    date = models.DateField()


class Product(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='prod_img', default='prod_img/no_image.png')
    permission = models.BooleanField(default=False)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username',blank=True ,null=True)


    def __str__(self):
        return self.title
  