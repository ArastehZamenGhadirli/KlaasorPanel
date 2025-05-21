from django.contrib import admin
from .models import Bootcamp , BootcampCategory , BootcampMembership , BootcampRegistrationRequest
# Register your models here.



admin.site.register(Bootcamp)
admin.site.register(BootcampCategory)
admin.site.register(BootcampMembership)
admin.site.register(BootcampRegistrationRequest)