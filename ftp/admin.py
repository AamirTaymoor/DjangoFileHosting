from django.contrib import admin
from .models import Profile, Directory, MyFiles
# Register your models here.
admin.site.register(Profile)
admin.site.register(Directory)
admin.site.register(MyFiles)