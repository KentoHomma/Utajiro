from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title
        
class Photo(models.Model):
    title = models.CharField(max_length=150)
    comment = models.TextField(blank=True)
    image = models.ImageField(upload_to ='photos', blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    #いいね機能一旦保留　like_num = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
'''   
いいねモデル一旦保留
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
'''
class UserInfoEdit(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    introduction = models.TextField(blank=True)
    icon = models.ImageField(upload_to ='userphotos', blank=True)
    def __str__(self):
        return self.username
