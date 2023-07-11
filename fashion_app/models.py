from django.db import models
from seller_app.models import *
# Create your models here.

class Register(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=100)
    conformpassword=models.CharField(max_length=100)
    propic=models.FileField(upload_to="media/", default="defult.jpg")

    def __str__(self):
        return self.email
    
class Cart(models.Model):
    product_id=models.ForeignKey(Listing_Catlog,on_delete=models.CASCADE)
    buyer_id=models.ForeignKey(Register,on_delete=models.CASCADE)
    qty=models.IntegerField(default=0)
    total=models.IntegerField(default=0)
    
    def __str__(self):
        return self.buyer_id
    
class Details(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    country=models.CharField(max_length=25)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=25)
    postcode=models.IntegerField(default=0)
    phone=models.IntegerField(default=0)
    email=models.CharField(max_length=50)
    buyer_id=models.ForeignKey(Register,on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname