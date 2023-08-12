import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email field is required !")
        if not username:
            raise ValueError("Username field is required !")
        if not password:
            raise ValueError("Password field is required !")
        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email, username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user
 
    def create_admin(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.save()
        return user
 
    def create_seller(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_seller = True
        user.save()
        return user
 
    def create_customer(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_customer = True
        user.save()
        return user

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    #adress = models.ManyToManyField(Address,on_delete=...)
    username = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(
        max_length=200, blank=False, null=False, unique=True)
    adress = models.ManyToManyField("Address")
    cards = models.ManyToManyField("cards")
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [] 

    def __unicode__(self):
        return str(self.username)
 
    def has_perm(self, perm, obj=None):
        return self.is_admin
 
    def has_module_perms(self, app_label):
        return True
    
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
    permission = models.BooleanField(default=False)
    image = models.ImageField(upload_to='prod_img', default='prod_img/no_image.png',)


    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='prod_img', default='prod_img/no_image.png',)




class updateCode(models.Model):
    successcode = models.CharField(max_length=6, default=0 )
    token = models.CharField(max_length=50)
    expire_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(minutes=5))
    used = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-expire_date']
