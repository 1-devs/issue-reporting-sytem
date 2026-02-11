from django.contrib.auth.models import AbstractUser, BaseUserManager
from .managers import CustomUserManager
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('CITIZEN', 'Citizen'),
        ('CELL_LEADER', 'Cell Leader'),
        ('SECTOR_LEADER', 'Sector Leader'),
        ('DISTRICT_LEADER', 'District Leader'),
    )
    
    username = None  # Remove username field
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CITIZEN')
    
    # Stores ID from Rwanda Administrative API
    assigned_location_id = models.IntegerField(null=True, blank=True)
    
    # Hierarchy logic: Cell Leader -> Sector Leader -> District Leader
    supervisor = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subordinates'
    )
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name' ,'phone_number']

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    def save(self, *args, **kwargs):
        # Logic: Ensure District Leaders only create Sector Leaders, etc.
        if self.supervisor:
            if self.role == 'SECTOR_LEADER' and self.supervisor.role != 'DISTRICT_LEADER':
                raise ValueError("Sector Leaders must be supervised by District Leaders.")
            if self.role == 'CELL_LEADER' and self.supervisor.role != 'SECTOR_LEADER':
                raise ValueError("Cell Leaders must be supervised by Sector Leaders.")
        super().save(*args, **kwargs)