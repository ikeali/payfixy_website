from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email.lower())
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('Superusers must have an email address.')

        user = self.create_user(email, password, **extra_fields)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    BUSINESS_TYPES = [
        ('for_profit', 'For Profit Business'),
        ('not_for_profit', 'Not For Profit Business'),
    ]

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(primary_key=False, default=uuid4)

    first_name = models.CharField(max_length=200, verbose_name="First Name")
    last_name = models.CharField(max_length=200, verbose_name="Last Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    # is_email_verified = models.BooleanField(default=False, verbose_name="Is Email Verified")
    is_staff = models.BooleanField(default=False, verbose_name="Is Staff")
    is_superuser = models.BooleanField(default=False, verbose_name="Is Superuser")

    # Merchant-specific fields
    business_type = models.CharField(
        max_length=20,
        choices=BUSINESS_TYPES,
        null=False,
        blank=True,
        verbose_name="Business Type"
    )
    business_name = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        verbose_name="Business Name"
    )
    country = models.CharField(max_length=100, null=False, verbose_name="Country")

    # Related fields for groups and permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name="Groups",
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name="User Permissions",
        blank=True,
        related_name='custom_user_permissions',
        related_query_name='custom_user_permissions',
    )

    # Customizing the authentication fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add fields here if they are required during user creation

    # Custom manager
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email



class OTP(models.Model):
    email = models.EmailField()  
    # code = models.CharField(max_length=6) 
    created_at = models.DateTimeField(auto_now_add=True) 
    expires_at = models.DateTimeField() 
    is_verified = models.BooleanField(default=False)


    def has_expired(self):
        return timezone.now() > self.expires_at