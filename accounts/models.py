from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, full_name, mobile, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not mobile:
            raise ValueError('Users must have an mobile number')

        if not full_name:
            raise ValueError('Users must have an full name')

        user = self.model(
            email=self.normalize_email(email),
            mobile=mobile,
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name, mobile, password=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email)
        )
        user = self.create_user(
            email,
            mobile=mobile,
            password=password,
            full_name=full_name,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, mobile, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            mobile=mobile,
            password=password,
            full_name=full_name,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    mobile = models.CharField(max_length=10, unique=True)
    timestamp = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that's built in.
    objects = UserManager()
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['full_name', 'email']  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.mobile

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


# hook in the New Manager to our Model
