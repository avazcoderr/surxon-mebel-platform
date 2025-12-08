import re

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from utils import validate_uzbekistan_phone


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        
        # Normalize phone number
        phone_number = self.normalize_phone(phone_number)
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(phone_number, password, **extra_fields)
    
    def normalize_phone(self, phone_number):
        """Normalize phone number to +998XXXXXXXXX format"""
        # Remove any spaces, hyphens, or parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', phone_number)
        
        # Add + if not present and starts with 998
        if cleaned.startswith('998') and not cleaned.startswith('+'):
            cleaned = '+' + cleaned
        elif not cleaned.startswith('+998'):
            if len(cleaned) == 9:  # Local format without country code
                cleaned = '+998' + cleaned
        
        return cleaned


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=False)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        validators=[validate_uzbekistan_phone],
        help_text='Enter phone number in format: +998XXXXXXXXX'
    )
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.phone_number})"
    
    def save(self, *args, **kwargs):
        # Normalize phone number before saving
        if self.phone_number:
            self.phone_number = CustomUserManager().normalize_phone(self.phone_number)
        super().save(*args, **kwargs)
