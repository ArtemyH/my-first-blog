from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.PostList.as_view(), name="post_list"),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    #url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.CreateComment.as_view(), name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/confirm/(?P<key>.+)/$', views.confirm_account, name='confirm_account'),
    url(r'^user/profile/$', views.PersonalAccount.as_view(), name='profile'),
    url(r'^user/posts/$', views.UserPostList.as_view(), name='user_post_list'),
    url(r'^user/post/new/$', views.CreateMyPost.as_view(), name='user_post_new'),
    url(r'^users_list/$', views.UsersList.as_view(), name='users_list'),
    url(r'^users_list/profile/(?P<pk>\d+)/$', views.UserDetailAndPosts.as_view(), name='user_detail'),    
    #url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^post/plus/$', views.PlusToPost.as_view(), name='plus_to_post'),
    url(r'^post/minus/$', views.MinusToPost.as_view(), name='minus_to_post'),
    
    
]