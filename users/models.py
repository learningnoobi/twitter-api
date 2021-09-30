from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email,username, password, **extra_fields):
        """
          Create and save a SuperUser with the given email,first name , lastname and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('Username must be set'))
        if not password:
            raise ValueError(_('Password must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email,first name , lastname and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email,username, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=200,unique=True)
    nickname = models.CharField(max_length=200,blank=True, null=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    following = models.ManyToManyField("self",symmetrical=False,related_name="followed" ,blank=True)
    bio = models.TextField(blank=True ,default="")
    avatar = models.ImageField(default='zenitsu.jpg', upload_to='avatars')
    cover_image = models.ImageField(default='cover.jpg', upload_to='avatars')
   

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    #requred for creating user
    REQUIRED_FIELDS = ['username','avatar']

    class Meta:
        ordering = ['-date_joined']
        verbose_name_plural="Custom Users"

    def __str__(self):
        return f'{self.username}'

    