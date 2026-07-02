from django.contrib.auth.models import User
from django.db import models


class Bounty(models.Model):
    STATUS_CHOICES = (
        ('wanted', 'Wanted'),
        ('captured', 'Captured'),
    )

    target_name = models.CharField(max_length=200)
    reward = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='wanted')
    location = models.CharField(max_length=200, blank=True)
    danger_level = models.CharField(max_length=50, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bounties')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.target_name} - {self.status}'
