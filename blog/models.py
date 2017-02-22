from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone


class PostManager(models.Manager):
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    objects = PostManager
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()  

    def __str__(self):
        return self.title
    
    
class MyPost(models.Model):
    author = models.ForeignKey('blog.ExtUser')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)    
    
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    
    
    def approve(self):
        self.approved_comment = True
        self.save()
                
    def __str__(self):
        return self.text   
    
    
class ExtUser(User):
    phone_number = models.CharField(max_length=20, blank=True)
    skype = models.CharField(max_length=30, null=True, blank=True)
    avatar = models.ImageField(upload_to='user_media', null=True, blank=True)
    activation_key = models.CharField(max_length=40, blank=True)
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return self.username
    
    
"""def set_email_as_unique():
    
    #Sets the email field as unique=True in auth.User Model
    
    email_field = dict([(field.name, field) for field in ExtUser._meta.fields])["email"]
    setattr(email_field, '_unique', True)

#this is called here so that attribute can be set at the application load time
set_email_as_unique()"""
    
#class UserProfile(models.Model):
    #user = models.OneToOneField(User, unique=True)
    
    #phone_number = models.CharField(max_length=12)
    #skype = models.CharField(max_length=30, null=True)
    #avatar = models.ImageField(null=True)
    
    #def __str__(self):
        #return self.user.username

