from django.contrib import admin
from .models import Post, MyPost, Comment, ExtUser, Category

admin.site.register(Post)
admin.site.register(MyPost)
admin.site.register(Comment)
admin.site.register(ExtUser)
admin.site.register(Category)
