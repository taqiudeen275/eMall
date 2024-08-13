from django.db import models
from accounts.models import User


class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.business_name


