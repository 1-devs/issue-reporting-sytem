from django.db import models
from django.conf import settings

class Issue(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('REPORTED_HIGHER', 'Reported to Higher Level'),
        ('SOLVED', 'Solved'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100) # e.g., Water, Electricity, Security...
    
    # Location data (IDs from Rwanda API)
    location_id = models.IntegerField() 
    reported_to_office = models.CharField(max_length=100) # e.g., "Kacyiru Cell"
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    comment = models.TextField(blank=True, null=True)
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