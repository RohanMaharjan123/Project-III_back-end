# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.choices import Choices
from .manager import CustomUserManager

ROLE_CHOICES = Choices("user", "admin")

class User(AbstractUser):
    # Remove the username field from AbstractUser
    username = None
    
    # Use email as the unique identifier, which is more common.
    # AbstractUser already defines first_name and last_name, which we can use.
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(
        _("Role"), max_length=20, choices=ROLE_CHOICES, default=ROLE_CHOICES.user
    )

    # Set email as the username field and remove username from required fields.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        """String representation of the user."""
        return str(self.email)

    def save(self, *args, **kwargs):
        """
        Ensure that is_staff is aligned with the user's role.
        A superuser is always a staff member with an admin role.
        """
        if self.is_superuser:
            self.role = ROLE_CHOICES.admin
            self.is_staff = True
        elif self.role == ROLE_CHOICES.admin:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == ROLE_CHOICES.admin

    @property
    def is_regular_user(self):
        return self.role == ROLE_CHOICES.user

    # The `set_password` method is already handled by AbstractBaseUser.
    # No need to override it unless you have custom logic.
    