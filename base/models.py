from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profileimage = models.ImageField(upload_to='profile_images',null=True,default="login_295128.png")
    firstname = models.CharField(max_length=200,null=True,blank=True)
    lastname = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=200,null=True,blank=True)
    phonenumber=models.CharField(max_length=20, null=True,blank=True)

    def __str__(self):
        return self.user.username

class Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contributionimage = models.ImageField(upload_to='contribution_images',null=True)
    created_at = models.DateTimeField(default=datetime.now)
    confirmation=models.CharField(max_length=300,null=True)

    def __str___(self):
        return self.user.username

class Month(models.Model):
    contribution = models.ForeignKey(Contribution, on_delete=models.CASCADE,null=True,blank=True)
    monthname = models.CharField(max_length=300)

def __str__(self):
    return self.user.username

class Chat(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    texts = models.CharField(max_length=1000000)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.texts

class Product(models.Model):
    productimage = models.ImageField(upload_to='product_images')
    productname = models.CharField(max_length=1000000)
    productprice = models.CharField(max_length=1000000)
    productdescription = models.CharField(max_length=1000000,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.productname