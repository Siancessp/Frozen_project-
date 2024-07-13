from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, Permission

class InfluencerManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone, password, **extra_fields)

class Influencer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    passbook = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, validators=[UnicodeUsernameValidator()])
    password = models.CharField(max_length=128)
    address = models.TextField()
    type = models.CharField(max_length=10)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=50, unique=True)
    status = models.BooleanField(default=True)

    # Required fields for AbstractBaseUser
    last_login = models.DateTimeField(default=timezone.now)

    objects = InfluencerManager()

    USERNAME_FIELD = 'phone'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_superuser(self):
        return self.status and self.is_staff

    @property
    def is_active(self):
        return self.status

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        verbose_name = 'Influencer'
        verbose_name_plural = 'Influencers'

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='influencer_groups',  # Adjust related_name to resolve clash
        related_query_name='influencer_group',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='influencer_user_permissions',  # Adjust related_name to resolve clash
        related_query_name='influencer_user_permission',
    )