from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.db import models
from django_countries.fields import CountryField

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

class User(AbstractBaseUser,PermissionsMixin):

    BUSINESS_TYPES = [
        ('for_profit', 'For Profit Business'),
        ('not_for_profit', 'Not For Profit Business'),
    ]

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Fields for merchants
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES, null=False, blank=True)
    business_name = models.CharField(max_length=100, null=False, blank=True)
    country = models.CharField(max_length=100, null=False)  # Check this

    # Related fields (such as groups and permissions)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',
        related_query_name='custom_user_permissions',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
