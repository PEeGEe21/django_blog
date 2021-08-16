from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, CreateView
from .models import Profile, FollowRequest
from django.contrib.auth.models import User
from blog.models import Comment, Post
from django.urls import reverse
from django.db.models import Q, query
from django.http import HttpResponse, response
import json
from autoslug import AutoSlugField
from django.http import HttpResponseRedirect
import random






# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profileEdit(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        
        'p_form': p_form,
        'u_form': u_form
    }

    return render(request, 'users/profile-edit.html', context)

@login_required
def profile(request):
    # post = get_object_or_404(Post, pk=pk)
    p = request.user.profile
    user = p.user
    sent_follow_requests = FollowRequest.objects.filter(from_user=p.user)
    rec_follow_requests = FollowRequest.objects.filter(to_user=p.user)
    followers = p.followers.all()
    user_posts = Post.objects.filter(author=user).order_by('-date_posted')
    user_comments = Comment.objects.filter(author=user)
    post_count = Post.objects.filter(author=user).order_by('-date_posted').count()

    print(rec_follow_requests, "rec_follow_requests")

    posts=Post.objects.all()       
    ctx={
        "posts":posts, 
        'user_posts': user_posts, 
        'user_comments': user_comments, 
        'followers_list': followers,
        'sent_follow_requests': sent_follow_requests,
        'rec_follow_requests': rec_follow_requests,
        'post_count': post_count
        }
    
    return render(request, 'users/profile.html', ctx)


@login_required
def like(request):
    # user = request.user
    if request.method == 'POST':
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            post_id = request.POST.get("post_id", None)
            post= get_object_or_404(Post, pk=post_id)
            if post.likes.filter(id=request.user.id):
                post.likes.remove(request.user)
                liked= False
            else:
                post.likes.add(request.user)
                liked=True
            ctx={"likes_count":post.total_likes, "liked":liked, "post_id":post_id}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    posts=Post.objects.all()
    already_liked=[]
    id=request.user.id
    for post in posts:
        if(post.likes.fliter(id=id).exists()):
            already_liked.append(post.id)
    ctx={"posts":posts, "already_liked": already_liked}


@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    # print(p, "p")
    u = p.user
    sent_follow_requests = FollowRequest.objects.filter(from_user=p.user)
    rec_follow_requests = FollowRequest.objects.filter(to_user=p.user)
    user_posts = Post.objects.filter(author=u).order_by('-date_posted')
    post_count = Post.objects.filter(author=u).order_by('-date_posted').count()
    print(rec_follow_requests)

    followers = p.followers.all()

    button_status = 'none'
    if p not in request.user.profile.followers.all():
        button_status = 'not_follower'

        if len(FollowRequest.objects.filter(from_user=request.user).filter(to_user=p.user)) == 1:
            button_status = 'follower_request_sent'

        
        if len(FollowRequest.objects.filter(from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'follower_request_received'

    context = {
        'u': u,
        'button_status': button_status,
        'followers_list': followers,
        'sent_follow_requests': sent_follow_requests,
        'rec_follow_requests': rec_follow_requests,
        'user_posts': user_posts,
        'post_count': post_count
    }

    return render(request, 'users/user_profile.html', context)

@login_required
def search_users(request):

    user=request.user   
    query = request.GET.get('q')
    object_list = User.objects.filter(username=query)
    rec_follow_requests = FollowRequest.objects.filter(to_user=user)

    # object_list_posts = Post.objects.filter(title=query, content=query)
    context = {
        'users': object_list,
        'rec_follow_requests': rec_follow_requests
        # 'posts': object_list_posts,
    }

    return render(request, 'users/search_users.html', context)


@login_required
def users_list(request):
    user=request.user
    users = Profile.objects.exclude(user=request.user)
    my_followers = request.user.profile.followers.all()
    rec_follow_requests = FollowRequest.objects.filter(to_user=user)


    
    sent_to = []
    followers = []
    for user in my_followers:
        follower = user.followers.all()
        for f in follower:
            if f in followers:
                follower = follower.exclude(user=f.user)
        followers += follower
    for i in my_followers:
        if i in followers:
            followers.remove(i)
    if request.user.profile in followers:
        followers.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in followers:
            random_list.remove(r)
    followers += random_list
    # for i in my_followers:
    #     if i in followers:
    #         followers.remove(i)
    # for se in sent_follow_requests:
    #     sent_to.append(se.to_user)
    context = {
        'users': followers,
        'sent': sent_to,
        'my_followers': my_followers,
        'rec_follow_requests': rec_follow_requests
    }
    return render(request, "users/users_list.html", context)


@login_required
def send_follower_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FollowRequest.objects.get_or_create(from_user=request.user, to_user=user)
    return HttpResponseRedirect('/users/profile/{}'.format(user.profile.slug))


@login_required
def cancel_follower_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest = FollowRequest.objects.filter(from_user=request.user, to_user=user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/profile/{}'.format(user.profile.slug))
    # return HttpResponseRedirect('/users/profile/{}'.format(user.profile.slug))


@login_required
def accept_follower_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FollowRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.followers.add(user2.profile)
    user2.profile.followers.add(user1.profile)
    if(FollowRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
        request_rev = FollowRequest.objects.filter(from_user=request.user, to_user=from_user).first()
        request_rev.delete()
    frequest.delete()
    return HttpResponseRedirect('/users/profile/{}'.format(request.user.profile.slug))


@login_required
def delete_follower_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FollowRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/profile/{}'.format(request.user.profile.slug))


def unfollow(request, id):
    user_profile = request.user.profile
    follower_profile= get_object_or_404(Profile, id=id)
    user_profile.followers.remove(follower_profile)
    follower_profile.followers.remove(user_profile)
    return HttpResponseRedirect('/users/profile/{}'.format(follower_profile.slug))


def follower_list(request):
    
    user=request.user
    rec_follow_requests = FollowRequest.objects.filter(to_user=user)
    p = request.user.profile
    followers = p.followers.all()
    context = {
        'followers': followers,
        'rec_follow_requests': rec_follow_requests
    }

    return render(request, "users/follower_list.html", context) 

def user_follower_list(request, id):
    p = Profile.objects.filter(id=id).first()
    u = request.user
    rec_follow_requests = FollowRequest.objects.filter(to_user=u)
    followers = p.followers.all()
    print(u, "u")
    button_status = 'none'
    if p not in request.user.profile.followers.all():
        button_status = 'not_follower'

        if len(FollowRequest.objects.filter(from_user=request.user).filter(to_user=p.user)) == 1:
            button_status = 'follower_request_sent'

        
        if len(FollowRequest.objects.filter(from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'follower_request_received'

    context = {
        'u': u,
        'followers': followers,
        'button_status': button_status,
        'rec_follow_requests': rec_follow_requests
    }

    return render(request, "users/user_follower_list.html", context) 

    


# class Profile(ListView):
#     model = Profile
#     template_name = 'blog/profile.html'
#     context_object_name = 'user'

#     def get_success_url(self):
#         return reverse('profile')