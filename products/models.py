from django.db import models
from business.models import Business



class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/categories', blank=True, null=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images')


class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def check_stock(self, quantity):
        return self.stock >= quantity

    def reduce_stock(self, quantity):
        if self.check_stock(quantity):
            self.stock -= quantity
            self.save()
            return True
        return False


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='images',null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"