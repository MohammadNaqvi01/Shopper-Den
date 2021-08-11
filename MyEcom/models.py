
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.db.models.fields import CharField
# Create your models here.


STATE_CHOICES=(
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Delhi','Delhi'),
    ('Up','Up'),
    ('Mp','Mp'),
    ('Maharashtra','Maharashtra'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Hyderabad','Hyderabad')
)


class Customer(models.Model):
    #field names of modelform should resemble model fields lol
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zip=models.IntegerField() 
    state=models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('E','Electronics'),
    ('W','Watch'),
    ('C','Cream')
)

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField(blank=True,null=True)
    discounted_price=models.FloatField(blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    brand=models.CharField(max_length=100,blank=True,null=True)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='producting')


    def __str__(self):
         return str(self.id)
     

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return   str(self.id)
@property
def total_cost(self):
    return self.quantity*self.product.selling_price





STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way','On the Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)


class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

class Confirm(models.Model):
      user=models.CharField(max_length=15)
      otp=models.IntegerField()