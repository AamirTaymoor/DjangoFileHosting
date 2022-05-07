from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<username>/<filename>
    return "%s%s" %(instance.user.username, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #my_files = models.FileField(upload_to=user_directory_path, blank=True)
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username

class Directory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, primary_key=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

class MyFiles(models.Model):
    file_path = models.FileField(upload_to=user_directory_path)
    directory = models.ForeignKey(Directory, null=True, on_delete=models.CASCADE)
    file_name=models.CharField(max_length=50, default='file.txt')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


def create_profile(sender, instance, created, **kwargs):
    if created:
       user_profile = Profile(user=instance)
       user_profile.save()

post_save.connect(create_profile, sender=User)
