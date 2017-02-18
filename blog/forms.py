from django import forms
from .models import Post, Comment, UserProfile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title','text',)
        
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('author', 'text',)
        
        
class MyUserFormRegistration(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username',)
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try: 
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Пользователь с таким адресом уже существует.')
        
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароль не совпадает.')
        return cd['password2']
    
    
    
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('avatar','phone_number','skype',)
        
        