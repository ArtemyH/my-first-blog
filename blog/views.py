from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import * #Post, Comment, ExtUser
from .forms import * #PostForm, CommentForm, ExtUserFormRegistration, AuthenticationFormWithEmail, ProfileForm
from django.contrib.auth.models import User

from django import forms
from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate

from django.core.mail import send_mail
from django.conf import settings
import hashlib, random

from django.http import HttpResponse


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
        except Exception:
            raise forms.ValidationError('Вход не удался.')
        if user is not None:
            auth_login(self.request, user)
            return redirect('profile')
        else:
            return redirect('login')
               
        return super(LoginFormView, self).form_valid(form)


class PersonalAccount(FormView):
    form_class = ProfileForm
    
    template_name = 'blog/user_profile_p.html'
    
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
        return render(request, 'blog/user_profile_p.html', {'form':form})
        
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
                
        return render(request, 'blog/user_profile_p.html', {'form':form})
        
    
    def form_valid(self, form):
        return super(PersonalAccount, self).form_valid(form)


class UserPostList(ListView):
    model = MyPost
    
    template_name = 'blog/user_post_list.html'
    
    def get_queryset(self):
        user = ExtUser.objects.get(email=self.request.user.email)
        return MyPost.objects.filter(author=user, status=MyPost.SUCCESSFUL_MODERATION)


class UsersList(ListView):
    model = ExtUser
    
    template_name = 'blog/users_list.html'    


class UserDetailAndPosts(DetailView):
    model = ExtUser
    
    template_name = 'blog/user_detail_and_posts.html'


class CreateMyPost(CreateView):
    form_class = MyPostForm
    template_name = 'blog/my_post_edit.html'
    success_url = '/'
    
    def send_mail_confirm(self, form):
        name = self.request.user.first_name
        email_subject = 'Создана публикация'
        email_body = "Пользователь %s создал публикацию \"%s\". Необходима модерация" % (name, form.instance.title)
        recievers = User.objects.filter(is_staff=True).values('email')
        send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['prime.95@mail.ru'], fail_silently=False)
    
    def form_valid(self, form):
        try:
            form.instance.author = ExtUser.objects.get(email=self.request.user.email)
        except ExtUser.DoesNotExist:
            form.instance.author = request.user
        self.send_mail_confirm(form)
        return super(CreateMyPost, self).form_valid(form)


class CreateComment(CreateView):
    form_class = CommentForm
    success_url = '/'
    template_name = 'blog/add_comment_to_post.html'
    
    #def form_valid(self, form):
        #try:
            #form.instance.author = ExtUser.objects.get(email=self.request.user.email)
        #except ExtUser.DoesNotExist:
            #form.instance.author = request.user        
        #return super(CreateComment, self).form_valid(form)
    
    def post(self, request, pk):
        post = get_object_or_404(MyPost, pk=pk)
        form = self.get_form()
        form.instance.post = post
        try:
            form.instance.author = ExtUser.objects.get(email=self.request.user.email)
        except ExtUser.DoesNotExist:
            form.instance.author = request.user
        comment = form.save()
        return redirect('post_detail', pk=pk)



class PlusToPost(TemplateView):
    
    def get(self, request):
        if request.is_ajax():
            post_pk = request.GET['post_pk']
            post = MyPost.objects.get(pk=post_pk)
            try:
                rating = Rating.objects.get(post=post, author=request.user)
            except Rating.DoesNotExist:
                rating = Rating.objects.create_rating(request.user, post)
            rating.add_plus()
            rating.save()
            post.count_rate()
            post.save()
        return HttpResponse(post.rate)


class MinusToPost(TemplateView):
    
    def get(self, request):
        if request.is_ajax():
            post_pk = request.GET['post_pk']
            post = MyPost.objects.get(pk=post_pk)
            try:
                rating = Rating.objects.get(post=post, author=request.user)
            except Rating.DoesNotExist:
                rating = Rating.objects.create_rating(request.user, post)
            rating.add_minus()
            rating.save()
            post.count_rate()
            post.save()
        return HttpResponse(post.rate)


def confirm_account(request, key):
    if request.user.is_authenticated():
        return redirect('/')
    
    user = get_object_or_404(ExtUser, activation_key=key)
    user.is_active = True
    user.save()
    return redirect('/')
    
    
def post_list(request):
    posts = MyPost.objects.all() #filter(published_date__lte=timezone.now()).order_by('published_date')
    #form = AuthenticationFormWithEmail()
    return render(request, 'blog/post_list.html', {'posts':posts})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})


def post_detail(request, pk):
    post = get_object_or_404(MyPost, pk=pk)
    return render(request, 'blog/my_post_detail.html', {'post':post})


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
    post = get_object_or_404(MyPost, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
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
            email = form.cleaned_data['email'].lower()
            username = email.split('@')[0]
            new_user = ExtUser.objects.create_user(username=username, email=email, password=form.cleaned_data['password'])
            #new_user.email = email
            new_user.is_active = False
            new_user.activation_key = hashlib.sha1(email.encode('utf-8')).hexdigest()
            new_user.save()
            
            host = request.get_host()
            email_subject = 'Подтверждение регистрации'
            email_body = "Здравствуйте %s, Благодарим за регистрацию. Для активации аккаунта перейдите по ссылке  http://%s/register/confirm/%s" % (username, host, new_user.activation_key)
            try:
                send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            except Exception:
                nothing = "to do"
                
            return redirect('/accounts/login')            
    else:
        form = ExtUserFormRegistration()
    return render(request, 'registration/register.html', {'form':form})



@login_required    
def personal_account(request):
    return redirect('post_list')




    
    
    
    
