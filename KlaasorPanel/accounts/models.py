from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class CustomUserManager(BaseUserManager):

    '''
    in this Model we can create superuser and normal user
    '''
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
    this class  inherited from AbstractBaseUser and is customized inorder to have related model
    i dont need is_superuser beacuse i extend this class from Abstarctuser
    
    """
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    Role_TYPE = {"Normal": "Normal", "Support": "Support", "SuperUser": "SuperUser"}
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    national_id = models.CharField(max_length=10, unique=True)
    gender = models.CharField(
        max_length=10, choices=[("male", "Male"), ("female", "Female")]
    )
    role = models.CharField(max_length=10, choices=Role_TYPE,default="Normal")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.phone_number
    
    
    
    