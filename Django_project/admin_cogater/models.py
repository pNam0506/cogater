from django.db import models
from WebSupport.models import Report
from django.contrib.auth.models import User

class Notification(models.Model):

    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
class Report(models.Model):

    username = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=[
            ("sent", "Sent"),
            ("read", "Read"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="sent"
    )

    created_at = models.DateTimeField(auto_now_add=True)  # เวลาที่ WebSupport ส่ง
    read_at = models.DateTimeField(null=True, blank=True) # เวลา Admin เปิดอ่าน
    approved_at = models.DateTimeField(null=True, blank=True)

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )