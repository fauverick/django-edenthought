from django.db import models

from django.contrib.auth.models import User

class Thought(models.Model):
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null=True)

class Profile(models.Model):
    profile_pic = models.ImageField(null = True, blank = True, default = 'default.jpeg', upload_to='media/') #allow user to not have a profile pic (profile_pic = none), otherwise there's gonna be bug
   
   #upload_to = 'media/' means uploading in the media folders in the object of the aws bucket edenthought-bucket-fauverick
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE, null=True)
