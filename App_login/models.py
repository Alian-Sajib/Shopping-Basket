from django.db import models

# To create a custom user model
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy

# To create automaticaaly one to one object with user and profile
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class MyUserManager(BaseUserManager):
    """A custom manager to deal with email as unique identifier"""

    def _create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password"""
        if not email:
            raise ValueError("The given email must be set")

        """Using many built-in function and variable here """

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        gettext_lazy("active"),
        default=False,
        help_text=gettext_lazy(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        gettext_lazy("active"),
        default=True,
        help_text=gettext_lazy(
            "Designates whether this user should be treated as active. Unselect this instead of deleting the user"
        ),
    )
    USERNAME_FIELD = "email"
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def __get_full_name__(self):
        return self.email

    def __get_short_name__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address_1 = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=30, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s Profile"

    """Check all fields are filled in """

    """ The f.name variable is used in the list comprehension [f.name for f in self._meta.get_field()] 
        to extract the names of all fields in the model. It is then used in the is_fully_filled method to 
        iterate over the field names and access their values."""

    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]
        for field in fields_name:
            if getattr(self, field) == None or getattr(self, field) == "":
                return False
        return True


"""use fields_name instead of field_names"""

"""when a user is created then a profile of that user created"""


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


"""change in user model also effect in profile model"""


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  # "profile" name same as related name
