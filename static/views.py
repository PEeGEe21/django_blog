from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like
from users.models import FollowRequest
from users.models import Profile
from .forms import CommentForm
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from django.contrib.auth.decorators import login_required

from .forms import PostCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, response, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
import json

# posts = [
#     {
#         'author': 'peegee',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2018'
#     },
#     {
#         'author': 'evido',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2018'
#     }
# ]

# Create your views here.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


# def like_view(request, pk):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     post.likes.add(request.user)
#     return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    # paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all().count()
        context['comments'] = comments
        if self.request.user.is_authenticated:
            rec_follow_requests = FollowRequest.objects.filter(to_user=self.request.user)
            context['rec_follow_requests'] = rec_follow_requests
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        # username = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super().get_context_data(*args,**kwargs)
        # context['user'] = User.objects.get(username=username)
        rec_follow_requests = FollowRequest.objects.filter(to_user=self.request.user)
        context['rec_follow_requests'] = rec_follow_requests
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


@login_required
def search_posts(request):
    query = request.Get.get('p')
    object_list = Post.objects.filter(tags_icontains=query)
    liked = [i for i in object_list if Like.objects.filter(user = request.user, post=i)]
    context = {
        'posts': object_list,
        'liked_post': liked
    }
    return render(request, "feed/search_posts.html", context)


@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()

        context = {
            'value': like.value,
            'likes': post_obj.liked.all().count(),
            # 'page': post_obj.liked.all(),
        }
        # return render(request, "blog/post_detail.html", context)
    # context={

    # }
    #     # return JsonResponse(data, safe=False)
    return redirect('like_post')
    # return render(request, "blog/post_detail.html")



# @login_required
# def like(request):
#     post_id = request.GET.get("likeId", "")
#     user = request.user
#     post = Post.objects.get(pk=post_id)
#     liked = False
#     liked = Like.objects.filter(user=user, post=post)
#     if like:
#         # like.delete()/
#         print('YOOOO')
#     else:
#         liked = True
#         Like.objects.create(user=user, post=post)
#     resp = {
#         'liked': liked
#     }
#     response = json.dumps(resp)
#     return HttpResponse(response, content_type = "application/json")
        # return JsonResponse({'liked': list(liked)})


# @login_required
# def like(request):
#     # user = request.user
#     if request.method == 'POST':
#         if request.POST.get("operation") == "like_submit" and request.is_ajax():
#             post_id = request.POST.get("post_id", None)
#             post= get_object_or_404(Post, pk=post_id)
#             if post.likes.filter(id=request.user.id):
#                 post.likes.remove(request.user)
#                 liked= False
#             else:
#                 post.likes.add(request.user)
#                 liked=True
#             ctx={"likes_count":post.total_likes, "liked":liked, "post_id":post_id}
#             return HttpResponse(json.dumps(ctx), content_type='application/json')
#     posts=Post.objects.all()
#     already_liked=[]
#     id=request.user.id
#     for post in posts:
#         if(post.likes.fliter(id=id).exists()):
#             already_liked.append(post.id)
#     ctx={"posts":posts, "already_liked": already_liked}
    # return render


def profile(request):
    return render(request, 'blog/user_profile.html', {'title': 'UserProfile'})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.filter(post=self.get_object()).order_by('date_added')
        context['comments'] = comments
        
        # stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        # print(stuff)
        # likes = stuff.likes.filter(username=self.request.user)
        # print(likes)
        # context['likes'] = likes
        # total_likes = stuff.likes.count()
        # sent_follow_requests = Post.objects.filter(id=self.kwargs['pk'])
        # user = get_object_or_404(User, username=self.kwargs.get('username'))

        # print(total_likes)

        # context['total_likes'] = total_likes
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm(instance=self.request.user)
            rec_follow_requests = FollowRequest.objects.filter(to_user=self.request.user)
            context['rec_follow_requests'] = rec_follow_requests

        return context

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'), author=self.request.user, post=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all().count()
        context['comments'] = comments
        if self.request.user.is_authenticated:
            rec_follow_requests = FollowRequest.objects.filter(to_user=self.request.user)
            context['rec_follow_requests'] = rec_follow_requests
        return context
# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'content']
#     form_class = PostCreationForm
#     template_name = 'blog/home.html'
#     context_object_name = User

    # def get_context_data(self, *args, **kwargs):
    #     username = self.request.session['username']
    #     context = super().get_context_data(*args,**kwargs)
    #     context['teacher'] = Teacher.objects.get(username=username)
    #     return context

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('post-create')

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all().count()
        context['comments'] = comments
        if self.request.user.is_authenticated:
            rec_follow_requests = FollowRequest.objects.filter(to_user=self.request.user)
            context['rec_follow_requests'] = rec_follow_requests
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all().count()
        context['comments'] = comments
        if self.request.user.is_authenticated:
            rec_follow_requests = FollowRequest.objects.filter(to_user=self.request.user)
            context['rec_follow_requests'] = rec_follow_requests
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class CommentDetailView(DetailView):
    model = Comment
    template_name = 'blog/comment_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all().count()
        context['comments'] = comments
        if self.request.user.is_authenticated:
            rec_follow_requests = FollowRequest.objects.filter(to_user=self.request.user)
            context['rec_follow_requests'] = rec_follow_requests
        return context
        
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all().count()
        context['comments'] = comments
        if self.request.user.is_authenticated:
            rec_follow_requests = FollowRequest.objects.filter(to_user=self.request.user)
            context['rec_follow_requests'] = rec_follow_requests
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_update.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments = Comment.objects.all().count()
        context['comments'] = comments
        if self.request.user.is_authenticated:
            rec_follow_requests = FollowRequest.objects.filter(to_user=self.request.user)
            context['rec_follow_requests'] = rec_follow_requests
        return context


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        #     def get_success_url(self):
        # return reverse('exam-create')

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})



# class UserProfilePostListView(ListView):
#     model = Post
#     template_name = 'users/profile.html'
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     # paginate_by = 

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.kwargs.get('username'))
#         return Post.objects.filter(author=user).order_by('-date_posted')

