from django import forms
from .models import Post, Comment, ExtUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class AuthenticationFormWithEmail(forms.ModelForm):
    email = forms.CharField(max_length=254, help_text='email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    
    class Meta:
        model = ExtUser
        fields = ('email', 'password',)

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ('title','text',)
        
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('author', 'text',)
        
        
class ExtUserFormRegistration(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    
    class Meta:
        model = ExtUser
        fields = ('email',)
        
    def clean_email(self):
        email = self.cleaned_data['email']
        try: 
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Пользователь с таким адресом уже существует.')
        
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароль не совпадает.')
        return cd['password2']
    
    
class ProfileForm(forms.ModelForm):
    
    
    class Meta:
        model = ExtUser
        fields = ('first_name', 'last_name', 'avatar', 'email', 'phone_number', 'skype',)
        widgets = {
            'avatar':forms.FileInput(),
        }
        
        
    
    

        