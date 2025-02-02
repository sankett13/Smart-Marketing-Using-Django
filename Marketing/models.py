from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class User_info(models.Model):
    name=models.CharField( max_length=50)
    email=models.EmailField( max_length=254)
    phone_number=PhoneNumberField()
    
    def __str__(self):
        return f"{self.name},{self.email},{self.phone_number}"
    
    
class Category(models.Model):
    category_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    product_name=models.CharField( max_length=100)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=20, decimal_places=2)
    available_stock=models.IntegerField()
    
    def __str__(self):
        return self.product_name
    
class user_history(models.Model):
    user_id=models.ForeignKey(User_info, on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    order_date=models.DateTimeField( auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_id.name} bought {self.product_id.product_name} "