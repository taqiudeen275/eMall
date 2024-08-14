from django.db import models
from django.conf import settings
from accounts.models import User
from business.models import Business


class Ad(models.Model):
    POSITION_CHOICES = [
        ('home', 'Home Page'),
        ('category', 'Category Page'),
        ('search', 'Search Results'),
        ('popup', 'Pop up')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='ad_images/')
    url = models.URLField()
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    clicks = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='created_ads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} by {self.created_by}'

    class Meta:
        ordering = ['-created_at']

    @property
    def is_current(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active