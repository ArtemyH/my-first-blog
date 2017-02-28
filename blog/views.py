from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import * #Post, Comment, ExtUser
from .forms import * #PostForm, CommentForm, ExtUserFormRegistration, AuthenticationFormWithEmail, ProfileForm
from django.contrib.auth.models import User

from django import forms
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate

from django.core.mail import send_mail
from django.conf import settings
import hashlib, random

from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder

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
            return redirect('profile', pk=user.pk)
        else:
            return redirect('login')
               
        return super(LoginFormView, self).form_valid(form)



class EditProfile(UpdateView):
    model = ExtUser
    form_class = ProfileForm
    template_name = 'blog/user_profile_p.html'
    
    def get_success_url(self):
        return reverse('profile', args=[self.object.pk])
    


class PostList(ListView):
    model = MyPost
    
    template_name = 'blog/post_list_sort.html'

    def get_queryset(self):
        return MyPost.objects.get_published_posts()

class UserPostList(ListView):
    model = MyPost
    
    template_name = 'blog/user_post_list.html'
    
    def get_queryset(self):
        user = ExtUser.objects.get(email=self.request.user.email)
        return MyPost.objects.get_published_posts().filter(author=user)


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
        email_body = "Пользователь %s создал публикацию \"%s\". Необходима модерация." % (name, form.instance.title)
        recievers = User.objects.filter(is_staff=True).values('email')
        send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, ['prime.95@mail.ru'], fail_silently=False)
    
    def form_valid(self, form):
        #obj = json.dumps((MyPost.objects.all().values('title', 'author__username')))
        #obj = serializers.serialize((MyPost.objects.all().values('title', 'author__username')))
        sd = json.dumps(list(MyPost.objects.all().values('title', 'author__username')), cls=DjangoJSONEncoder)
        print(sd)
        try:
            form.instance.author = ExtUser.objects.get(email=self.request.user.email)
        except ExtUser.DoesNotExist:
            form.instance.author = request.user
        self.send_mail_confirm(form)
        return super(CreateMyPost, self).form_valid(form)


class DetailMyPost(DetailView):
    model = MyPost
    template_name = 'blog/my_post_detail.html'
    context_object_name = 'post'


class CreateComment(CreateView):
    form_class = CommentForm
    success_url = '/'
    template_name = 'blog/add_comment_to_post.html'
    
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


def post_list_sort(request):
    #queryset = MyPost.objects.get_published_posts()
    if request.is_ajax():
        field = request.GET['field']
        order = request.GET['order']
        if field == 'author':
            if order == 'asc':
                queryset = MyPost.objects.get_published_posts().order_by('author__username').values(
                    'pk', 'author', 'author__username', 'title', 'published_date', 'description')
            elif order == 'desc':
                queryset = MyPost.objects.get_published_posts().order_by('-author__username').values(
                    'pk', 'author', 'author__username', 'title', 'published_date', 'description')
        elif field == 'published_date':
            if order == 'asc':
                queryset = MyPost.objects.get_published_posts().order_by('published_date').values(
                    'pk', 'author', 'author__username', 'title', 'published_date', 'description')
            elif order == 'desc':
                queryset = MyPost.objects.get_published_posts().order_by('-published_date').values(
                    'pk', 'author', 'author__username', 'title', 'published_date', 'description')
    
    sd = json.dumps(list(queryset), cls=DjangoJSONEncoder)
    
    return JsonResponse(sd, safe=False)
    
        
    


def confirm_account(request, key):
    if request.user.is_authenticated():
        return redirect('/')
    
    user = get_object_or_404(ExtUser, activation_key=key)
    user.is_active = True
    user.save()
    return redirect('/')
    
    
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
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')



@login_required
def comment_remove(requst, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
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






    
    
    
    
