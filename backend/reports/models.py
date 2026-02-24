from django.db import models
from django.conf import settings

class Issue(models.Model):
    # Categories based on your project requirements
    CATEGORY_CHOICES = [
        ('WATER', 'Water Supply'),
        ('ROAD', 'Road/Infrastructure'),
        ('ELECTRICITY', 'Electricity'),
        ('SECURITY', 'Security'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('ESCALATED', 'Reported to Higher Level'),
        ('SOLVED', 'Solved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Location data (ID from the external Rwanda API)
    location_id = models.IntegerField() 
    location_name = models.CharField(max_length=255) # e.g., "Kigali > Gasabo > Kacyiru"
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    comment = models.TextField(blank=True, null=True) # Latest leader comment
    photo = models.ImageField(upload_to='issue_photos/', blank=True, null=True)
    
    # Relationships
    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='my_reports'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"