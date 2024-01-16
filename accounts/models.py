from django.db import models
from django.contrib.auth.models import AbstractUser
from .usermanager import UserManager
import random
import string

def generate_unic_code():
    cod_length = 6
    characters = string.ascii_letters + string.digits

    while(True):
        code = ''.join(random.choice(characters) for _ in range(cod_length)) 
        
        if not User.objects.filter(personal_id=code).exists():
            return code


class User(AbstractUser):
    GENDER = (
        ('m', 'مرد'),
        ('w', 'زن')
    )
    username = None
    profile_picture = models.ImageField(upload_to='accounts/', null=True)
    referral_code = models.CharField(max_length=6, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, choices=GENDER)
    province = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    national_id = models.CharField(null=True, max_length=10)
    post_id = models.CharField(null=True, max_length=9)
    born_dateTime = models.DateField(null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_shope = models.BooleanField(null=True, default=False)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []
    backend = 'accounts.backend.MobileBackend'
