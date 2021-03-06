from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField
from users.models import Profile

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # likes = models.ManyToManyField(User, blank=True, related_name='blog_posts')
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')

    objects = models.Manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()

    # @property
    # def total_likes(self):
    #     return self.likes.count()
    @property
    def num_likes(self):
        return self.liked.all().count()



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_added= models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']
    
    def get_absolute_url(self):
        return reverse('comment-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.post.title} - {self.author}'

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return f"{self.user}-{self.post}-{self.value}"

# class Like(models.Model):
#     user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)