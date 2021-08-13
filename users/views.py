from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, CreateView
from .models import Profile
from django.contrib.auth.models import User
from blog.models import Post
from django.urls import reverse
from django.db.models import Q, query
from django.http import HttpResponse, response
import json
from autoslug import AutoSlugField






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
    user = request.user
    print(user.id)
    user_posts = Post.objects.filter(author=user)
    if request.method == 'POST':
        user = request.user
        user_posts = Post.objects.filter(author=user)
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            post_id = request.POST.get("post_id", None)
            post= get_object_or_404(Post, pk=post_id)
            if post.likes.filter(id=request.user.id):
                post.likes.remove(request.user)
                liked= False
                print(liked, "liked")
            else:
                post.likes.add(request.user)
                liked=True
            ctx={"likes_count":post.total_likes, "liked":liked, "post_id":post_id, 'user_posts': user_posts,}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        posts=Post.objects.all()
        already_liked=[]
        id=request.user.id
        for post in posts:
            if(post.likes.filter(id=id).exists()):
                already_liked.append(post.id)
                
        ctx={"posts":posts, "already_liked": already_liked,  'user_posts': user_posts}
        print(already_liked)
        print(user_posts)
        # context = {
        #     'user_posts': user_posts,
        # }
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
    print(p, "p")
    u = p.user
    user_posts = Post.objects.filter(author=u)

    context = {
        'u': u,
        'user_posts': user_posts
    }

    return render(request, 'users/user_profile.html', context)

@login_required
def search_users(request):
    query = request.GET.get('q')
    object_list = User.objects.filter(username=query)
    context = {
        'users': object_list
    }

    return render(request, 'users/search_users.html', context)
    


# class Profile(ListView):
#     model = Profile
#     template_name = 'blog/profile.html'
#     context_object_name = 'user'

#     def get_success_url(self):
#         return reverse('profile')