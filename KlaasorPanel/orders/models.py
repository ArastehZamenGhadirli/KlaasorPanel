from django.db import models
from accounts.models import CustomUser 
from django.conf import settings
# Create your models here.

class BootcampCategory(models.Model): #دسته بندی بوتکمپ
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Bootcamp(models.Model):
    class State(models.TextChoices):
        DRAFT = 'draft', 'پیش نویس'
        REGISTRATION = 'registering', 'در حال ثبت نام'
        ONGOING = 'ongoing', 'در حال برگزاری'
        COMPLETED = 'completed', 'برگزار شده'
        CANCELLED = 'cancelled', 'لغو شده'

    name = models.CharField(max_length=255)
    category = models.ForeignKey(BootcampCategory, on_delete=models.CASCADE, related_name='bootcamps')
    start_date = models.DateField()
    held_days = models.CharField(max_length=100)  
    held_time = models.CharField(max_length=50)  
    capacity = models.PositiveIntegerField()
    state = models.CharField(max_length=20, choices=State.choices, default=State.DRAFT)
    
    def __str__(self):
        return f"{self.name} - {self.get_state_display()}"



class BootcampMembership(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'student', 'دانشجو'
        MENTOR = 'mentor', 'منتور'
        TEACHER = 'teacher', 'مدرس'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bootcamp_memberships')
    bootcamp = models.ForeignKey('Bootcamp', on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=Role.choices)

    class Meta:
        unique_together = ('user', 'bootcamp', 'role')
        
        
        
        

class BootcampRegistrationRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'بررسی نشده'
        IN_REVIEW = 'in_review', 'در حال بررسی'
        APPROVED = 'approved', 'تأیید شده'
        REJECTED = 'rejected', 'رد شده'

    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name='registration_requests')
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} | {self.bootcamp.name} | {self.get_status_display()}"

