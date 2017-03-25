from django.contrib.auth.models import Permission, User,AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db import models
#from simple_history.models import HistoricalRecords
from django.contrib.admin import widgets
from django.db.models.signals import post_save
from django.dispatch import receiver

# class Author(models.Model):
#     user = models.OneToOneField(User,unique=True)
#     email = models.EmailField(blank=True)
#     phone = models.BigIntegerField(null=True)
#
#     def create_user_profile(sender,instance,created,**kwargs):
#         if created:
#             Author.objects.create(user=instance)
#
#     post_save.connect(create_user_profile,sender=User)
#
#     def __str__(self):
#         return self.user
#
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff_account=None, activation_key=None, key_expires=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        user = self.model(
            email=self.normalize_email(email),
            activation_key=activation_key,
            key_expires=key_expires
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, activation_key=None, key_expires=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            activation_key=activation_key,
            key_expires=key_expires,
        )
        user.is_approved = True
        user.is_active = True
        user.is_superuser = True
        user.has_filled_data = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    has_filled_data = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
    objects = CustomUserManager()
   # history = HistoricalRecords()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

class Owner(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(unique=True, max_length=7)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)
    dob = models.DateField(verbose_name='Date of Birth', null=True)
    phone_number = models.CharField(max_length=10)
    avatar = models.ImageField('profile pic (1:1 square)', upload_to='owner-uploaded-images', null=True, blank=True)

    def __str__(self):
        name = str(self.first_name)
        if self.middle_name != None:
            name += ' '
            name += self.middle_name
        name += ' '
        name += self.last_name
        return name

    def get_user_name(self):
        return self.username

class Note(models.Model):

    PRIORITY=(
        ('1', 'NO'),
        ('2', 'LOW'),
        ('3', 'MEDIUM'),
        ('4', 'HIGH'),
    )
    user = models.OneToOneField(CustomUser)
    title = models.CharField(max_length=500)
    create_date = models.DateTimeField(auto_now_add=True)
    reminder_date = models.DateField()
    is_important = models.BooleanField(default=False)
    priority =models.CharField(max_length=1,choices=PRIORITY,null=True)


    def __str__(self):
        return str(self.title)


class List(models.Model):
    note = models.ForeignKey(Note,default=1)
    item = models.CharField(max_length=250)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return self.item
