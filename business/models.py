from django.db import models
from accounts.models import User

class Business(models.Model):
    BUSINESS_CATEGORIES = [
        ('retail', 'Retail'),
        ('service', 'Service'),
        ('manufacturing', 'Manufacturing'),
        # Add more categories as needed
    ]
    
    BUSINESS_SIZES = [
        ('small', 'Small (1-50 employees)'),
        ('medium', 'Medium (51-250 employees)'),
        ('large', 'Large (250+ employees)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # New fields
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    
    category = models.CharField(max_length=100, choices=BUSINESS_CATEGORIES, blank=True)
    
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    
    founded_date = models.DateField(blank=True, null=True)
    
    size = models.CharField(max_length=10, choices=BUSINESS_SIZES, blank=True)
    
    operating_hours = models.TextField(blank=True)
    
    tax_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.business_name