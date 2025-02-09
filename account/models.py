from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None):
        """Creates and returns a regular user with an email and password."""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """Creates and returns a superuser with all permissions."""
        user = self.create_user(email, password=password, user_type="admin")
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ("customer", "Customer"),
        ("vendor", "Vendor"),
        ("admin", "Admin"),
    )

    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Returns True if the user has the given permission."""
        return True  

    def has_module_perms(self, app_label):
        """Returns True if the user has permissions for the given app."""
        return True
