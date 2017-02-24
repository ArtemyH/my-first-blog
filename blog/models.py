from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone

from django.core.mail import send_mail
from django.conf import settings


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
    IN_MODERATION = 'IM'
    SUCCESSFUL_MODERATION = 'SM'
    REJECTED_MODERATION = 'RM'
    MODERATION_STATUSES = (
        (IN_MODERATION, 'In moderation'),
        (SUCCESSFUL_MODERATION, 'Succesful moderation'),
        (REJECTED_MODERATION, 'Rejected')
    )
    
    author = models.ForeignKey('blog.ExtUser')
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)    
    status = models.CharField(choices=MODERATION_STATUSES, max_length=2, default=IN_MODERATION)
    rejected_reason = models.TextField(default="", blank=True)
    rate = models.IntegerField(default=0)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_status = self.status
        
    def __str__(self):
        return self.title
    
    def count_rate(self):
        marks = Rating.objects.filter(post=self)
        value = 0
        for mark in marks:
            value += mark.value
        self.rate = value
            
        
    def save(self, *args, **kwargs):
        if self.status != self.REJECTED_MODERATION:
            self.rejected_reason = ""
            
        if self.status != self.prev_status:
            email = self.author.email
            name = self.author.first_name
            
            if self.status == self.SUCCESSFUL_MODERATION:
                email_subject = 'Ваша запись опубликована'
                email_body = "Привет, %s! Ваша запись \"%s\" опубликована." % (name, self.title)
                send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            
            elif self.status == self.REJECTED_MODERATION:
                email_subject = 'Ваша запись отклонена'
                email_body = "Привет, %s! Ваша запись \"%s\" отклонена.\nПричина: %s." % (name, self.title, self.rejected_reason)
                send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
                
        return super().save(*args, **kwargs)
    
    
class Comment(models.Model):
    post = models.ForeignKey('blog.MyPost', related_name='comments')
    author = models.ForeignKey('blog.ExtUser')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
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


class RatingManager(models.Manager):
    def create_rating(self, author, post):
        mark = self.create(author=author, post=post)
        return mark
    

class Rating(models.Model):
    value = models.IntegerField(default=0)
    post = models.ForeignKey('blog.MyPost')
    author = models.ForeignKey('auth.User') 
    
    objects = RatingManager()
    
    def add_plus(self):
        if self.value < 1:
            self.value += 1
        else:
            self.value = 1
        
    def add_minus(self):
        if self.value > -1:
            self.value += -1
        else:
            self.value = -1
            
    def __str__(self):
        return self.value
    
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

