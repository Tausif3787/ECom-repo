from django.db import models

#to create a custom user model and admin panel

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext_lazy
# Create your models here.

#to automatically create one to one relations

from django.db.models.signals import post_save
from django.dispatch import receiver

#BaseUserManager er kaaz hocce amra je user gulo create kori ta handle kore
class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields): #bulding func

        if not email:
            raise ValueError("The email must be set!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        ugettext_lazy('staff status'),
        default=False,
        help_text=ugettext_lazy('Designates whether the user can log in this site')
    )

    is_active = models.BooleanField(
        ugettext_lazy('Active'),
        default=True,
        help_text=ugettext_lazy('Designates whether the user should be treated as active. Unselect this instead of deleting accounts')
    )

    USERNAME_FIELD ='email'
    objects = MyUserManager()

    #user name, short name, fullname etc sob kisur jonno email jate return kora hoye tai rewrite kora hocce
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address = models.TextField(max_length=300, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zipcode = models.CharField(max_length=10,blank=True)
    country = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=20,blank=True)
    date_join = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s Profile'"
    def is_fully_filed(self): #check korbe sob gulo filed fillup hoyese kina...eita ekta building func
        fields_names = [f.name for f in self._meta.get_fields()]

        for fields_name in fields_names:
            value = getattr(self, fields_name)
            if value is None or value=='':
                return False
        return True

#automatically jokhon new user create hobe automatically profile tar user create hoye jabe and user er sathe linked hoye jabe...views.py te gia OneToOneField e kaaz
#kora lageb na

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):

    if created:#jodi user model create kora hoye
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() #profile and user er related_name er name o profile.eita 2ta same hote hobe. 67line. eita dia user model er jekono change hole profile model o change hobe
