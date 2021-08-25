from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, CommentDeleteView, CommentUpdateView, CommentDetailView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('user/profile/', views.profile, name='user-profile'),
    # path('like/', views.like, name='post-like'),
    # path('like/', views.like_view, name='like_post'),
    path('like/', views.like_unlike_post, name='like_post'),
    # path('user/profile/', views.UserProfilePostListView.as_view(template_name='users/profile.html'), name='user-profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('about/', views.about, name='blog-about'),
]

