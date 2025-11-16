from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as username"""
    username = None
    email = models.EmailField(unique=True)
    
    # Music preferences
    favorite_genres = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="List of favorite music genres"
    )
    favorite_artists = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list,
        help_text="List of favorite artist names or IDs"
    )
    moods = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="User mood preferences (energetic, calm, happy, etc.)"
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email


# Keep UserProfile for backward compatibility or remove if not needed
class UserProfile(models.Model):
    """Legacy model - can be removed if migrating to User model completely"""
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    favorite_genres = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="List of favorite music genres"
    )
    favorite_artists = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list,
        help_text="List of favorite artist names or IDs"
    )
    moods = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="User mood preferences (energetic, calm, happy, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"
