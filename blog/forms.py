from django import forms
from .models import Post, Comment, MyUser

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title','text',)
        
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('author', 'text',)
        
        
class MyUserFormRegistration(forms.ModelForm):
    
    class Meta:
        model = MyUser
        fields = ('username', 'password',)