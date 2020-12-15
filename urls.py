from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('post/<post_title>', views.view_post, name='view_post'),
    path('post/<post_title>/like', views.like_post, name='like_post'),
    path('post/<str:post_title>/comment',  views.add_comment, name='add_comment'),
    path('profile/<str:user_name>', views.view_profile, name='profile'),
    path('profile/<str:user>/settings', views.settings, name='settings'),


    
    path('search/', views.search, name='search'),
    path('update_profile/<current_user>', views.update_profile, name='update_profile'),
    path('change_image/<user>', views.change_image, name='change_image'),
    path('delete_user/<user>', views.delete_user, name='delete_user'),
    path('follow/<str:user_name>', views.follow_user, name='follow'),

    path('write_post/', views.WritePostView.as_view(), name='write_post'),
    path('delete/<post_title>', views.delete_post, name='delete_post'),





    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('contact/', views.contact, name='contact'),
]