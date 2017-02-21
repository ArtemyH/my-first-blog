from django.contrib import admin
from .models import Post, Comment, ExtUser

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ExtUser)
