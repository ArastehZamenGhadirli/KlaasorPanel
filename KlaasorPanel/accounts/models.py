from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
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
        return self.create_user(phone_number, password, **extra_fields)

class Team(models.Model):
    class TeamRole(models.TextChoices):
        NORMAL = 'NORMAL', 'Normal User'
        FINANCIAL = 'FINANCIAL', 'Financial Support'
        TICKET = 'TICKET', 'Ticket Support'
        REGISTER = 'REGISTER', 'Registration Support'
        MENTOR = 'MENTOR', 'Mentor'
        TEACHER = 'TEACHER', 'Teacher'
        SUPERUSER = 'SUPERUSER', 'Super User'
    
    name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=10,
        choices=TeamRole.choices,
        unique=True
    )
    permissions_group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        null=True,  # Allow null initially
        blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        if not self.permissions_group_id:  # Only for new teams
            group = Group.objects.create(name=f"{self.role}_Permissions")
            self.permissions_group = group
        super().save(*args, **kwargs)

class CustomUser(AbstractBaseUser):
    # Core fields
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11, unique=True)
    national_id = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")])
    
    # Team relationship
    team = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    
    # Status fields
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone_number} ({self.team.get_role_display() if self.team else 'No Team'})"

    def save(self, *args, **kwargs):
        if not self.team_id:  # Assign to Normal team by default
            self.team = Team.objects.filter(role='NORMAL').first()
        super().save(*args, **kwargs)
        self._sync_permissions()

    def _sync_permissions(self):
        """Sync user permissions with their team"""
        self.groups.clear()
        if self.team and self.team.permissions_group:
            self.groups.add(self.team.permissions_group)
            # Update staff/superuser status without recursive save
            CustomUser.objects.filter(pk=self.pk).update(
                is_staff=self.team.role != 'NORMAL',
                is_superuser=self.team.role == 'SUPERUSER'
            )

    @property
    def is_staff(self):
        return hasattr(self, 'team') and self.team.role != 'NORMAL'

    @property
    def is_superuser(self):
        return hasattr(self, 'team') and self.team.role == 'SUPERUSER'

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return self.groups.filter(permissions__codename=perm).exists()

    def has_module_perms(self, app_label):
        return self.is_staff or self.is_superuser

    # Helper properties
    @property
    def is_mentor(self):
        return self.team.role == 'MENTOR'

    @property
    def is_teacher(self):
        return self.team.role == 'TEACHER'

    @property
    def is_financial_support(self):
        return self.team.role == 'FINANCIAL'

    @property
    def is_ticket_support(self):
        return self.team.role == 'TICKET'

    @property
    def is_register_support(self):
        return self.team.role == 'REGISTER'