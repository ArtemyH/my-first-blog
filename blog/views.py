from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment, ExtUser
from .forms import PostForm, CommentForm, ExtUserFormRegistration, AuthenticationFormWithEmail, ProfileForm
from django.contrib.auth.models import User

from django import forms
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate


class LoginFormView(FormView):
    form_class = AuthenticationFormWithEmail
    
    template_name = 'registration/login.html'
    
    success_url = "/"
    
        
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        try:
            user = authenticate(username=email, password=password)
        except User.MultipleObjectsReturned:
            raise forms.ValidationError('Почта не уникальна.')
        if user is not None:
            auth_login(self.request, user)            
               
        return super(LoginFormView, self).form_valid(form)


class PersonalAccount(FormView):
    form_class = ProfileForm
    
    template_name = 'blog/profile_p.html'
    
    success_url = 'profile'
    
    
    #@login_required
    def get(self, request):
        user = ExtUser.objects.get(email=request.user.email.lower())
        form = ProfileForm(initial={'first_name': user.first_name, 
                                    'last_name': user.last_name, 
                                    'email': user.email,
                                    'skype': user.skype,
                                    'avatar': user.avatar,
                                    'phone_number': user.phone_number,})
        #form.fields['skype'] = 'cregt'
        return render(request, 'blog/profile_p.html', {'form':form, 'avatar':user.avatar.url})
        
    def post(self, request):
        user = ExtUser.objects.get(email=request.user.email.lower())
        form = ProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            cd = form.cleaned_data
            user.first_name = cd['first_name'] 
            user.last_name = cd['last_name'] 
            user.skype = cd['skype'] 
            user.phone_number = cd['phone_number'] 
            user.avatar = cd['avatar']
            #user.avatar.save('avatar.jpg', form.avatar)
            #if user.is_changed():
            user.save()
                
        return render(request, 'blog/profile_p.html', {'form':form, 'avatar':user.avatar})
        
    
    def form_valid(self, form):
        return super(PersonalAccount, self).form_valid(form)
    

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #form = AuthenticationFormWithEmail()
    return render(request, 'blog/post_list.html', {'posts':posts})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return render(request, 'blog/post_detail.html', {'post':post})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form':form})


@login_required
def comment_remove(requst, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    post_pk = comment.post.pk
    return redirect('blog.views.post_detail', pk=post_pk)


def register(request):
    if request.method == "POST":
        form = ExtUserFormRegistration(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            new_user = ExtUser.objects.create_user(username=username, email=email, password=form.cleaned_data['password'])
            #new_user.email = email
            new_user.save()
            return redirect('/accounts/login')            
    else:
        form = ExtUserFormRegistration()
    return render(request, 'registration/register.html', {'form':form})



@login_required    
def personal_account(request):
    return redirect('post_list')




    
    
    
    
