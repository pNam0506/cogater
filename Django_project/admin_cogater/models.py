from django.db import models
from WebSupport.models import Report

class Notification(models.Model):

    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
class Report(models.Model):

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )