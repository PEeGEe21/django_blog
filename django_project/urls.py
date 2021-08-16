"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from users import views as user_views
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    # path('profile/', user_views.profile, name='profile'),
    path('profile/', user_views.profile, name='profile'),
    path('users/profile/<slug>/', user_views.profile_view, name='profile_view'),
    path('followers/', user_views.follower_list, name='follower_list'),
    path('users/followers/<int:id>', user_views.user_follower_list, name='user_follower_list'),
    path('users/follow-request/send/<int:id>/', user_views.send_follower_request, name='send_follower_request'),
    path('users/follow-request/cancel/<int:id>/', user_views.cancel_follower_request, name='cancel_follower_request'),
    path('users/follow-request/accept/<int:id>/', user_views.accept_follower_request, name='accept_follower_request'),
    path('users/follow-request/delete/<int:id>/', user_views.delete_follower_request, name='delete_follower_request'),
    path('users/unfollow/<int:id>/', user_views.unfollow, name='unfollow'),
    path('users/', user_views.users_list, name='users_list'),
    # path('profile/', user_views.Profile.as_view(template_name='users/profile.html'), name='profile'),
    path('profile-edit/', user_views.profileEdit, name='profile_edit'),
    path('search-users/', user_views.search_users, name='search_users'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('', include('blog.urls')),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
